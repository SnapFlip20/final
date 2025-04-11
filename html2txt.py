import requests
from bs4 import BeautifulSoup
import re



def sep_no(s):
    #print(s)
    if s[0] in ['I', 'V', 'X']:
        tnum, txt = '', ''
        dot_idx = -1
        if '.' in s: # I.
            dot_idx = s.find('.')
            tnum += s[:dot_idx+2]
            txt = s[dot_idx+2:]
        elif '-' in s: # I-
            dot_idx = s.find('-')
            tnum += s[:dot_idx+2]
            txt = s[dot_idx+2:]
        else:
            # I II III IV V VI VII VIII IX X
            if s.startswith('IIntroduction') or s.startswith('IINTRODUCTION'):
                tnum += 'I'
                txt = 'Introduction'
            elif s.startswith('III'): # 3
                tnum += 'III'
                txt = s[3:].strip()
            elif s.startswith('II') and not s.startswith('IIntro'): # 2
                tnum += 'II'
                txt = s[2:].strip()
            elif s.startswith('IX'): # 9
                tnum += 'IX'
                txt = s[1:].strip()
            elif s.startswith('IV'): # 4
                tnum += 'IV'
                txt = s[2:].strip()
            elif s.startswith('I'): # 1
                tnum += 'I'
                txt = s[1:].strip()
            elif s.startswith('VIII'): # 8
                tnum += 'VIII'
                txt = s[4:].strip()
            elif s.startswith('VII'): # 7
                tnum += 'VII'
                txt = s[3:].strip()
            elif s.startswith('VI'): # 6
                tnum += 'VI'
                txt = s[2:].strip()
            elif s.startswith('V'): # 5
                tnum += 'V'
                txt = s[1:].strip()
            elif s.startswith('X'): # 10
                tnum += 'X'
                txt = s[1:].strip()
            else:
                txt = s

        seperated = (tnum, txt)
        return seperated

    else:
        rematch = re.match(r'^((?:IV|IX|V?I{0,3})(?:\.\d+)?|\d+(?:\.\d+)?)([A-Z].+)$', s)
        if rematch:
            tnum, txt = rematch.groups()
        else:
            tnum, txt = re.sub(r'(\d)([A-Za-z])', r'\1. \2', s)
        
        if tnum == '':
            tnum = '0'
        
        seperated = (tnum, txt)
        return seperated

def extract(url):
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    sections = []

    now = {'title': 'default', 'paragraphs': []}

    for element in soup.find_all(['h1', 'h2', 'h3', 'h6', 'p']):
        if element.name == 'h6': # abstract
            title_text = element.get_text(strip=True)
            title_text = sep_no(title_text)
            now = {
                'title': title_text,
                'paragraphs': []
            }
            #print(title_text)

        elif element.name in ['h1', 'h2', 'h3', 'h6']: # title number + title name
            if now['paragraphs']:
                sections.append(now)
            title_text = element.get_text(strip=True)
            title_text = sep_no(title_text)
            now = {
                'title': title_text,
                'paragraphs': []
            }
            #print(title_text)

        elif element.name == 'p': # paragraph
            paragraph = element.get_text(strip=True)

            # except LaTeX expression
            if paragraph and not re.search(r'[\$]|\\\(|\\\)', paragraph):
                now['paragraphs'].append(paragraph)

    # last section
    if now['paragraphs']:
        sections.append(now)

    return sections



url = "https://arxiv.org/html/2504.07495v1"

# execute
sections = extract(url)

for sec in sections:
    print(sec['title'])
    #print("\n".join(sec['paragraphs']))
    #print("\n")


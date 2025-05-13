import sys
import requests
from bs4 import BeautifulSoup
import re



def sep_no(s):
    if s[0] in ['I', 'V', 'X']:
        tnum, txt = '', ''
        dot_idx = -1
        if '.' in s: # I.A or I.1
            dot_idx = s.find('.')
            tnum += s[:dot_idx+2]
            txt = s[dot_idx+2:]
        elif '-' in s: # I-A or I-1
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
    
    elif s[0].isdigit():
        dot_idx = 0
        for i in s:
            if i.isalpha():
                break
            dot_idx += 1
        
        tnum, txt = s[:dot_idx], s[dot_idx:]
        seperated = (tnum, txt)
        return seperated
    
    else: # maybe references section
        tnum, txt = '0', s
        seperated = (tnum, txt)
        return seperated



def extract(url):
    if len(url) < 1:
        print('error: invalid url', file=sys.stderr)
        return

    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    sections = []

    now = {'title': 'default', 'paragraphs': []}

    for element in soup.find_all(['h1', 'h2', 'h3', 'h6', 'p']):
        if element.name == 'h6': # abstract
            title_text = ('0', element.get_text(strip=True))
            now = {
                'title': title_text,
                'paragraphs': []
            }

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



url = ""

"""
sections = extract(url)

if sections:
    for sec in sections:
        if sec['title'][1] != 'References':
            print(*sec['title'])
            print('\n'.join(sec['paragraphs']))
        print()
"""

# execute
def main(url):
    sections = extract(url)
    fout = open(f'extracted_{url[-10:]}.txt', 'w', encoding='UTF-8')
    if sections:
        for sec in sections:
            if sec['title'][1] != 'References':
                fout.write(sec['title'][0] + ' ' + sec['title'][1] + '\n')
                for i in sec['paragraphs']:
                    fout.write(i + '\n')
            fout.write('\n')
    fout.close()

"""

sections =
[
    {
        'title' = (index, title) -> tuple,
        'paragraph' = [context1, context2, ... , context9] -> list
    } -> dict
    ...
    {
        'title' = (index, title),
        'paragraph' = [context1, context2, ... , context9]
    }
] -> list

"""

main(url)

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



import sys
import requests
from bs4 import BeautifulSoup
import re



def sep_no(s):
    if s[0] in ['I', 'V', 'X']:
        tnum, txt = '', ''
        dot_idx = -1
        if '.' in s[:6]: # I.A or I.1
            dot_idx = s.find('.')
            tnum += s[:dot_idx+2]
            txt = s[dot_idx+2:]
        elif '-' in s[:6]: # I-A or I-1
            dot_idx = s.find('-')
            tnum += s[:dot_idx+2]
            txt = s[dot_idx+2:]
        else:
            # I II III IV V VI VII VIII IX X XI XII XIII
            if s == 'Introduction' or s == 'INTRODUCTION':
                tnum = s
                txt = ''
            elif s.startswith('IIntro') or s.startswith('IINTRO'):
                tnum += 'I'
                txt = s[1:]
            elif s.startswith('III'): # 3
                tnum += 'III'
                txt = s[3:].strip()
            elif s.startswith('II'): # 2
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
            elif s.startswith('XIII'): # 13
                tnum += 'XIII'
                txt = s[4:].strip()
            elif s.startswith('XII'): # 12
                tnum += 'XII'
                txt = s[3:].strip()
            elif s.startswith('XI'): # 11
                tnum += 'XI'
                txt = s[2:].strip()
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
    
    elif 'abstract' in s.lower():
        tnum, txt = 'Abstract', ''
        seperated = (tnum, txt)
        return seperated
    
    else:
        tnum, txt = '', s
        seperated = (tnum, txt)
        return seperated



def extract(url):
    global title
    if len(url) < 1:
        print('error: invalid url', file=sys.stderr)
        return

    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    sections = []

    now = {'title': ('', ''), 'paragraphs': ['']}
    h3_exception = False

    for element in soup.find_all(['h1', 'h2', 'h3', 'h6', 'p']):
        txtline = element.get_text(strip=True)

        if element.name in ['h1', 'h2', 'h3', 'h6']:
            if 'reference' in txtline.lower():
                break

            if element.name == 'h6': # abstract
                if now['paragraphs'] and not h3_exception:
                    sections.append(now)

                title_text = txtline
                title_text = sep_no(title_text)

                if title_text[0] == '':
                    h3_exception = True
                else:
                    h3_exception = False
            
                now = {
                    'title': title_text,
                    'paragraphs': ['']
                }
            
            elif element.name == 'h1': # main title
                title_text = txtline
                title = title_text
                now = {
                    'title': ('Title', title_text),
                    'paragraphs': ['']
                }

            elif element.name in ['h2', 'h3']: # title number + title name
                if now['paragraphs'] and not h3_exception:
                    sections.append(now)

                title_text = txtline
                title_text = sep_no(title_text)
                
                if title_text[0] == '':
                    h3_exception = True
                else:
                    h3_exception = False

                now = {
                    'title': title_text,
                    'paragraphs': ['']
                }

        elif element.name == 'p': # paragraph
            paragraph = txtline
            if not h3_exception and not h3_exception:
                now['paragraphs'].append(paragraph)



    # add last section
    if now['paragraphs'] and not h3_exception:
        sections.append(now)

    return sections

def main(url):
    sections = extract(arxiv_url)
    if sections:
        print()
        for sec in sections:
            # reference는 출력 제외
            if sec['title'][1] == 'References':
                continue

            if sec['title'][0] == 'Title':
                print(*sec['title'])
            else:
                if sec['title'][0]:
                    print(*sec['title'])
                else:
                    print(sec['title'][1])
                #print(*sec['paragraphs'])



arxiv_url = ''

if __name__ == "__main__":
    main(arxiv_url)

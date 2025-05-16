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
                tnum = ''
                txt = s
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
    
    else: # maybe references section
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

    now = {'title': ('', ''), 'paragraphs': []}

    for element in soup.find_all(['h1', 'h2', 'h3', 'h6', 'p']):
        if element.name == 'h6': # abstract
            if now['paragraphs']:
                sections.append(now)

            title_text = element.get_text(strip=True)
            now = {
                'title': ('', title_text),
                'paragraphs': []
            }
        
        elif element.name == 'h1': # main title
            title_text = element.get_text(strip=True)
            now = {
                'title': ('', 'Title'),
                'paragraphs': [title_text]
            }

        elif element.name in ['h2', 'h3']: # title number + title name
            if now['paragraphs']:
                sections.append(now)

            title_text = element.get_text(strip=True)
            title_text = sep_no(title_text)
            now = {
                'title': title_text,
                'paragraphs': []
            }

        elif element.name == 'p': # paragraph
            paragraph = element.get_text(strip=True)
            now['paragraphs'].append(paragraph)

    # add last section
    if now['paragraphs']:
        sections.append(now)

    return sections


"""
sections = extract(url)
    fout = open(f'extracted_{url[-12:]}.txt', 'w', encoding='UTF-8')

    fout.write(title + '\n\n') # title
    if sections:
        for sec in sections:
            if sec['title'][1] == 'References':
                continue

            if sec['title'][0]:
                fout.write(sec['title'][0] + ' ')
            fout.write(sec['title'][1] + '\n')
            for i in sec['paragraphs']:
                fout.write(i + '\n')
            fout.write('\n')
    fout.close()
"""



# execute
def main(url):
    sections = extract(url)

    if sections:
        print()
        for sec in sections:
            # reference는 출력 제외
            if sec['title'][1] == 'References':
                continue

            # print title
            if sec['title'][0]:
                print(*sec['title'])
                ...
            else:
                print(sec['title'][1])
                ...

            # print paragraph        
            print('\n'.join(sec['paragraphs']))
            print()



url = ""

if __name__ == "__main__":
    main(url)

import os
import sys
import re

def rmNextLine(list):
    for idx, elem in enumerate(list):
        if '\n' in elem:
            new_elem = str(elem).replace('\n','')
        else:
            new_elem = elem
        list[idx] = new_elem
    return list

def rmNum(list):
    for idx, elem in enumerate(list):
        # Match all char with only numbers
        regex = r'^\d+$'
        new_elem = re.sub(regex,'',elem)
        list[idx] = new_elem
    return list

def reformatTime(lines):
    # Match all --> a....
    regex = r'-->.+'
    lines = [ re.sub(regex,'',x) for x in lines ]
    lines = [ x.strip() for x in lines ]
    
    # for idx, elem in enumerate(lines):
    hms_regex = r'(\d+:){2}\d+.\d+'
    lines = [changeTimeFormat(x) if re.search(hms_regex,x) else x for x in lines ]

    return lines

def changeTimeFormat(time):
    h, m, s = str(time).split(':')
    m = int(m) + 60 * int(h)

    MM = f'0{m}' if len(str(m)) == 1 else m
    # zfill amke sures that the result has at least 5 char, else pad with zeros
    SS = "{:.2f}".format(float(s)).zfill(5)

    return f'[{MM}:{SS}]'

def vtt2lrc(file):
    with open(file,'r',encoding='utf-8') as f:
        lines = f.readlines()

    lines = rmNextLine(lines)
    lines = rmNum(lines)
    lines = list(filter(lambda x:x != '', lines))  
    lines = list(filter(lambda x:x != 'WEBVTT', lines))
    lines = list(filter(lambda x:x != 'Telegram@djyqlfy', lines))
    lines = reformatTime(lines)
    final_lines = []

    for idx, itm in enumerate(lines):
        if (idx) % 2 == 0:
            final_lines.append(f'{itm}{lines[idx+1]}')

    final_lines = '\n'.join(final_lines)
    output_name, extension = os.path.splitext(file)
    with open(f'{output_name}.lrc','a',encoding='utf-8') as f:
        f.writelines(final_lines)

    print(final_lines)

if __name__ == '__main__':
    # if len(sys.argv != 2):
    #     Exception('Usage: vtt2lrc <> <>')
    
    for file in os.listdir():
        if file.endswith('.vtt'):
            vtt2lrc(file)

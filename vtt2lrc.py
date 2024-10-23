import os
import sys
import re

def rmNextLine(list):
    for idx, elem in enumerate(list):
        if '\n' in elem:
            new_elem = str(elem).replace('\n','')
            print(list[-1])
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
    
    for idx, elem in enumerate(lines):
        

        

    return lines

def changeTimeFormat(time):
    h, m, s = str(time).split(':')
    m += int(m) + 60 * int(h)

def vtt2lrc(file):
    with open(file,'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines = rmNextLine(lines)
        lines = rmNum(lines)
        lines = list(filter(lambda x:x != '', lines))  
        lines = list(filter(lambda x:x != 'WEBVTT', lines))
        lines = list(filter(lambda x:x != 'Telegram@djyqlfy', lines))
        lines = reformatTime(lines)
        print(lines)

if __name__ == '__main__':
    # if len(sys.argv != 2):
    #     Exception('Usage: vtt2lrc <> <>')
    
    for file in os.listdir():
        if file.endswith('.vtt'):
            vtt2lrc(file)
    # for file in os.listdir():
    #     vtt2lrc(file)

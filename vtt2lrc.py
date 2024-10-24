import os
import re

def rmNextLine(lines):
    for idx, elem in enumerate(lines):
        if '\n' in elem:
            new_elem = str(elem).replace('\n','')
        else:
            new_elem = elem
        lines[idx] = new_elem
    return lines

def rmNum(lines):
    for idx, elem in enumerate(lines):
        regex = r'^\d+$'
        new_elem = re.sub(regex,'',elem)
        lines[idx] = new_elem
    return lines

def isTimeStamp(line):
    regex = r'^\[\d{2}:\d{2}.\d{2}\]$'
    if re.match(regex,line):
        return True
    return False

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
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = rmNextLine(lines)

    lines = list(filter(lambda x: x != '', lines))  
    lines = list(filter(lambda x: x != 'WEBVTT', lines))
    lines = list(filter(lambda x: x != 'Telegram@djyqlfy', lines))
    lines = reformatTime(lines)

    final_lines = []

    for idx, itm in enumerate(lines):
        if idx + 1 < len(lines):
            if isTimeStamp(itm):
                final_lines.append(itm)
            elif not(isTimeStamp(itm)) and not(isTimeStamp(lines[idx + 1])):
                final_lines[-1] += itm
        else:
            final_lines[-1] += itm
                
    final_lines = '\n'.join(final_lines)
        
    print(final_lines)
    output_name = ''
    if '.wav.vtt' in file:
        output_name = file.replace('.wav.vtt','')
    else:
        output_name, _ = os.path.splitext(file)

    with open(f'{output_name}.lrc', 'a', encoding='utf-8') as f:
        f.write(final_lines + '\n')

if __name__ == '__main__':
    for file in os.listdir():
        if file.endswith('.vtt'):
            vtt2lrc(file)

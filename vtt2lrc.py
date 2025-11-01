import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import json
from pathlib import Path
import sys

ignore_phrases = []

# Folder containing the .exe
if getattr(sys, 'frozen', False):
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path(__file__).parent  # running from script

IGNORE_FILE = EXE_DIR / "ignore_phrases.json"

# Ensure file exists
if not IGNORE_FILE.exists():
    IGNORE_FILE.write_text("[]", encoding="utf-8")

def loadIgnoreFile():
    global ignore_phrases
    if IGNORE_FILE.exists():
        try:
            with open(IGNORE_FILE,'r',encoding='utf-8') as f:
                ignore_phrases = json.load(f)
        except Exception:
            ignore_phrases = []
    else:
        ignore_phrases = []
    
def rmNextLine(lines):
    for idx, elem in enumerate(lines):
        if '\n' in elem:
            new_elem = str(elem).replace('\n','')
        else:
            new_elem = elem
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
    # Clean up the string of each line, removing any extra spaces before and after
    lines = [ x.strip() for x in lines ]
    # for idx, elem in enumerate(lines):
    # Regex match dd:dd:dd.dddd
    hms_regex = r'(\d+:){2}\d+.\d+'
    # If any of the line matches the timestamp, change the timestamp line into lrc format
    lines = [changeTimeFormat(x) if re.search(hms_regex,x) else x for x in lines ]
    return lines

def changeTimeFormat(time):
    # Split the string of timestamp based on : hh:mm:ss.sss
    h, m, s = str(time).split(':')
    # Convert hours into minute as lrc have no hour
    m = int(m) + 60 * int(h)
    # Put 0 infront of the minute if the minute is less than 10
    MM = f'0{m}' if len(str(m)) == 1 else m
    # fill make sures that the result has at least 5 char, else pad with zeros
    SS = "{:.2f}".format(float(s)).zfill(5)
    return f'[{MM}:{SS}]'

def vtt2lrc(tgt_file, folder):
    with open(tgt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Removes all next line in between lines when read, return an array of lines without \n
    lines = rmNextLine(lines)
    # If the line before removing \n is only \n then, remove the line entirely as after removing \n, it is now a empty string in the array
    lines = list(filter(lambda x: x != '', lines))

    # Removes other constants
    for phrase in ignore_phrases:
        lines = list(filter(lambda x: x != phrase, lines))
    # Reformat the way timestamp is represented in vtt to lrc 
    lines = reformatTime(lines)
    
    result = []

    for idx, itm in enumerate(lines):
        if idx + 1 < len(lines):
            if isTimeStamp(itm):
                result.append(itm)
            # If the current line is not a timestamp but the previous line is, then it is a line of lyrics
            elif not(isTimeStamp(itm)) and (isTimeStamp(lines[idx - 1])):
                result[-1] += itm
        else:
            result[-1] += itm
                
    result = '\n'.join(result)
        
    output_name = ''
    if '.wav.vtt' in tgt_file:
        output_name = tgt_file.replace('.wav.vtt','')
    else:
        output_name, _ = os.path.splitext(tgt_file)

    with open(f'{output_name}.lrc', 'w', encoding='utf-8') as f:
        f.write(result + '\n')

    return output_name + '.lrc'

def on_close():
    root.destroy()
    os._exit(0)

def getAllVttFiles(folder, result=None):
    if result is None:
        result = []
    for file in os.listdir(folder):
        full_path = os.path.join(folder,file)
        
        if file.endswith('.vtt'):
            output = vtt2lrc(full_path, folder)
            result.append(output)
        elif os.path.isdir(full_path):
            getAllVttFiles(full_path, result)
            
    return result

def open_folder():
    loadIgnoreFile()
    folder = filedialog.askdirectory(title='Select Folder with .vtt Files in it')
    if not folder:
        return

    converted_files = getAllVttFiles(folder)
    
    if converted_files:
        messagebox.showinfo("Done",f"Converted {len(converted_files)} .vtt files to .lrc:\n\n" + "\n".join(os.path.basename(f) for f in converted_files))
    else:
        messagebox.showinfo("No Files","No .vtt files found in the selected Folder")

def open_ignore():
    if not IGNORE_FILE.exists():
        with open(IGNORE_FILE,'w',encoding='utf-8') as f:
            f.write("[]")
    try:
        os.startfile(IGNORE_FILE)
    except Exception:
        print(f"Error: could not find {IGNORE_FILE}!")
        

# GUI setup
root = tk.Tk()
root.title("VTT to LRC Converter")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW",on_close)

label = tk.Label(root, text="Click to select a folder with .vtt files")
label.pack(padx=10)

btn = tk.Button(root, text="Select Folder", command=open_folder, height=2, width=30)
btn.pack(pady=20)

label = tk.Label(root, text="Click to open/create an ignore phrase folder")
label.pack(padx=10)

btn = tk.Button(root, text="Open ignore_phrases.json ", command=open_ignore, height=2, width=30)
btn.pack(pady=20)

loadIgnoreFile()
root.mainloop()
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

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
 
def vtt2lrc(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Removes all next line in between lines when read, return an array of lines without \n
    lines = rmNextLine(lines)
    # If the line before removing \n is only \n then, remove the line entirely as after removing \n, it is now a empty string in the array
    lines = list(filter(lambda x: x != '', lines))
    # Removes other constants
    lines = list(filter(lambda x: x != 'WEBVTT', lines))
    lines = list(filter(lambda x: x != 'Telegram@djyqlfy', lines))
    # Reformat the way timestamp is represented in vtt to lrc 
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
        
    output_name = ''
    if '.wav.vtt' in file:
        output_name = file.replace('.wav.vtt','')
    else:
        output_name, _ = os.path.splitext(file)

    with open(f'{output_name}.lrc', 'a', encoding='utf-8') as f:
        f.write(final_lines + '\n')

    return output_name + '.lrc'

def on_close():
    root.destroy()
    os._exit(0)

def open_folder():
    folder = filedialog.askdirectory(title='Select Folder with .vtt Files in it')
    if not folder:
        return
    
    converted_files = []
    for file in os.listdir(folder):
        if file.endswith('.vtt'):
            full_path = os.path.join(folder,file)
            output = vtt2lrc(full_path)
            converted_files.append(output)

    if converted_files:
        print(converted_files)
        messagebox.showinfo("Done",f"Converted {len(converted_files)} .vtt files to .lrc:\n\n" + "\n".join(os.path.basename(f) for f in converted_files))
    else:
        messagebox.showinfo("No Files","No .vtt files found in the selected Folder")

# GUI setup
root = tk.Tk()
root.title("VTT to LRC Converter")
root.geometry("300x150")
root.protocol("WM_DELETE_WINDOW",on_close)

label = tk.Label(root, text="Click to select a folder with .vtt files")
label.pack(padx=10)

btn = tk.Button(root, text="Select Folder", command=open_folder, height=2, width=20)
btn.pack(pady=40)

root.mainloop()
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkmsgbox
import copy
import re
import datetime
from shutil import copy2 as shutilcopy2

def is_pic(filename):  # checks if file is a picture according to its extension
    pic_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  
    _, extension = os.path.splitext(filename)
    return extension.lower() in pic_extensions

def is_video(filename):  # checks if file is a picture according to its extension
    pic_extensions = ['.avi','.mp4']  
    _, extension = os.path.splitext(filename)
    return extension.lower() in pic_extensions

def get_date_time_from_name(filename): #searches and extracts a date_time pattern in the filename
    regex = r'_2[0-9][0-9][0-9](?:1[0-2]|0[1-9])(?:0[1-9]|[12]\d|3[01])_(?:[01][0-9]|2[0-3])[0-5][0-9][0-5][0-9]'  # searches
    match = re.search(regex, filename)
    if match:
        return match.group()
    else:
        return None
    
def check_exists_ask_overwrite(destpath):
    if os.path.exists(destpath):
        path = os.path.dirname(destpath)
        name, ext = os.path.splitext(os.path.basename(destpath))
        answer = tkmsgbox.askyesnocancel(title="file " + name + ext + " exists already", message="overwrite?")
        if answer == False: 
            i = 2
            regex = r'\([2-9]\)'
            if re.search(regex, name) == True:
                regex = r'[2-9]'
                match = re.search(regex, name)
                i = int(match.group()) + 1
            destpath = os.path.join(path, name + "(" + str(i) + ")" + ext)
            destpath = check_exists_ask_overwrite(destpath)
        elif answer == None:
            destpath = None
    return destpath

rootW = tk.Tk()
rootW.withdraw()  # Hide the root window

# Open a file dialog for opening a file
work_path = filedialog.askdirectory()

dir_list = os.listdir(work_path)
dir_list = list(filter(lambda x: os.path.isdir(os.path.join(work_path, x)), dir_list))

for folder in dir_list:
    act_folderpath = os.path.join(work_path, folder)
    pic_list = [file for file in os.listdir(act_folderpath) if is_pic(file) or is_video(file)] 
    newname_list = copy.deepcopy(pic_list)
    for i, pic in enumerate(pic_list):
        pic_name, pic_ext = os.path.splitext(pic)
        if is_video(pic):
            tmp_name = "VID" 
        else:
            tmp_name = "IMG"
        tmp_datetimepatrn = get_date_time_from_name(pic_name)
        if tmp_datetimepatrn == None: # take creation time if not in name already
            creation_time_sec1970 = os.path.getctime(os.path.join(act_folderpath, pic))
            ctm = datetime.datetime.fromtimestamp(creation_time_sec1970)
            tmp_datetimepatrn = "_" + str(ctm.year * 10000 + ctm.month * 100 + ctm.day) + "_" + ("" if ctm.hour > 9 else "0") + str(ctm.hour) + str(ctm.minute * 100 + ctm.second)
            tmp_info = pic_name[pic_name.find("_") : ]
        else:
            tmp_info = pic_name[pic_name.find(tmp_datetimepatrn)+len(tmp_datetimepatrn) : ]
        tmp_name = tmp_name + tmp_datetimepatrn + "__" + tmp_info
        if pic.find("PANO") > -1:
            tmp_name = tmp_name + "_" + "PANO"
        tmp_name = tmp_name + "_" + folder + pic_ext
        newname_list[i] = tmp_name
        
    for i, pic in enumerate(pic_list):
        act_destpath = os.path.join(work_path, newname_list[i])
        act_destpath = check_exists_ask_overwrite(act_destpath)
        print(pic)
        print(newname_list[i])
        if act_destpath == None:
            print("skiped!\n")
        else:
            try:
                #shutilcopy2(os.path.join(act_folderpath, pic), act_destpath)
                print("OK (copied successful)")
            except Exception as e:
                print("error:" + str(e))
            finally:
                print('\n')
import os
import copy
import re
import datetime
import tkinter.messagebox as tkmsgbox

from shutil import copy2 as shutilcopy2

import helperfunctions as hlpfnc

def check_exists_ask_overwrite(destpath):
    if os.path.exists(destpath):
        path = os.path.dirname(destpath)
        name, ext = os.path.splitext(os.path.basename(destpath))
        answer = tkmsgbox.askyesnocancel(title="file " + name + ext + " exists already", message="overwrite? YES=overwrite, NO=copy, CANCEL=skip that file")
        if answer == False: 
            i = 2
            regex = r'\([2-9]\)'
            match0 = re.search(regex, name)
            if  match0:
                regex = r'[2-9]'
                match = re.search(regex, match0.group())
                i = int(match.group()) + 1
                name = name[0 : str(name).rfind("(")]
            name = name + "(" + str(i) + ")" 
            destpath = os.path.join(path, name + ext)
            destpath = check_exists_ask_overwrite(destpath)
        elif answer == None:
            destpath = None
    return destpath

def merge_pics_from_sourcefolders(workpath):
    item_list = os.listdir(workpath)
    dir_list = list(filter(lambda x: os.path.isdir(os.path.join(workpath, x)), item_list))
    act_folderpath = workpath
    for folder in dir_list:
        act_folderpath = os.path.join(workpath, folder)
        pic_list = [file for file in os.listdir(act_folderpath) if hlpfnc.is_pic(file) or hlpfnc.is_video(file)] 
        newname_list = copy.deepcopy(pic_list)
        for i, pic in enumerate(pic_list):
            pic_name, pic_ext = os.path.splitext(pic)
            if hlpfnc.is_video(pic):
                tmp_name = "VID" 
            else:
                tmp_name = "IMG"
            tmp_datetimepatrn = hlpfnc.get_date_time_from_name(pic_name)
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
            act_destpath = os.path.join(workpath, newname_list[i])
            act_destpath = check_exists_ask_overwrite(act_destpath)
            print(pic)
            if act_destpath != None:
                print(os.path.basename(act_destpath))
            else:
                print(newname_list[i])
            if act_destpath == None:
                print("skiped!\n")
            else:
                try:
                    shutilcopy2(os.path.join(act_folderpath, pic), act_destpath)
                    print("OK (copied successful)")
                except Exception as e:
                    print("error:" + str(e))
                finally:
                    print('\n') 
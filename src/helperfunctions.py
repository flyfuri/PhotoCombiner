import os
import re
import datetime

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
        return match.group()[1 : ]
    else:
        return None
    
def filenamedatetm_to_timestamp(filenamedatetm):
    dtm = datetime.datetime(int(filenamedatetm[0:4]),
                            int(filenamedatetm[4:6]),
                            int(filenamedatetm[6:8]),
                            int(filenamedatetm[9:11]),
                            int(filenamedatetm[11:13]),
                            int(filenamedatetm[13:]))
    tstamp_sec1970 = int(dtm.timestamp())
    return tstamp_sec1970

def timestamp_to_filenamedatetm(timestamp):
    dtm = datetime.datetime.fromtimestamp(timestamp)
    tmp_datetimepatrn = (("" if dtm.year > 9 else "0") + str(dtm.year) 
                            + ("" if dtm.month > 9 else "0") + str(dtm.month)
                            + ("" if dtm.day > 9 else "0") + str(dtm.day) + "_"
                            + ("" if dtm.hour > 9 else "0") + str(dtm.hour) 
                            + ("" if dtm.minute > 9 else "0")+ str(dtm.minute) 
                            + ("" if dtm.second > 9 else "0") + str(dtm.second))
    return tmp_datetimepatrn

def extract_sources_piclist(piclist):
    sourcelist = []
    for pic in piclist:
        pic_name, _ = os.path.splitext(pic)
        source = pic_name.split("_")[-1]
        if source not in sourcelist:
            sourcelist.append(source)
    return sourcelist

def create_timeline_table(piclist):
    table = []
    dimension2 = []
    first_entry = True
    table.clear()
    for pic in piclist:
        pic_name, pic_ext = os.path.splitext(pic)    
        pic_date_time = get_date_time_from_name(pic_name)
        if pic_date_time is not None:
            pic_stamp = filenamedatetm_to_timestamp(pic_date_time)
            pic_stamp_new = filenamedatetm_to_timestamp(pic_date_time)
            pic_source = pic_name.split("_")[-1]
            record = [pic_name, pic_stamp, pic_stamp_new, pic_source, pic_ext]
            source_index = -1
            if first_entry:
                dimension2.clear()
                dimension2.append(record)
                table.append(dimension2)
                first_entry = False
            else:
                for i in range(len(table)):
                    if table[i][0][3] == pic_source:
                        source_index = i
                if source_index < 0:
                    dimension2.clear()
                    dimension2.append(record)
                    table.append(dimension2)
                else:
                    tablerec = list(table[source_index])
                    tablerec.append(record)
                    table[source_index] = tablerec

    return table   

def calc_tline_minmax(tline_table):
    min= tline_table[0][0][1]
    max = tline_table[0][0][1]
    for source in tline_table:
        for record in source:
            for i in range(1,2):
                tmpval = record[i] 
                if tmpval < min:
                    min = tmpval
                elif tmpval > max:
                    max = tmpval
    minmax = {}
    minmax[min] = min
    minmax[max] = max
    return minmax

def calc_tline_minmax_pixel(canvas_start,canvas_end, tlinemin, tlinemax):
    pix_minmaxfactor = {}
    factor = (canvas_end-canvas_start) / (tlinemax-tlinemin)
    minpix = canvas_start
    maxpix = canvas_start + (tlinemax-tlinemin)*factor 
    pix_minmaxfactor[minpix] = minpix
    pix_minmaxfactor[maxpix] = maxpix
    pix_minmaxfactor[factor] = factor
    return pix_minmaxfactor


def get_source_index(table, source):
    index = -1
    for i in range(len(table)):
        if table[i][0][3] == source:
            index = i
            break
    return index


def get_picname_index(table_one_source, name):
    index = -1
    for i in range(len(table_one_source)):
        if table_one_source[i][0] == name:
            index = i
            break
    return index

def rename_moved_files(timeline_table, workpath):
    if timeline_table is not None:
        for sources in timeline_table:
            for pic in sources:
                if pic[1] != pic[2]:
                    old_name = str(pic[0]) + pic[4]
                    new_name = old_name.replace(timestamp_to_filenamedatetm(pic[1]), timestamp_to_filenamedatetm(pic[2]))
                    os.rename(os.path.join(workpath, old_name), os.path.join(workpath, new_name)) 


if __name__ == '__main__': # test
    filedt = "20230325_145622"
    stamp = filenamedatetm_to_timestamp(filedt)
    print(stamp)    
    print(timestamp_to_filenamedatetm(stamp))
import os
import re
import datetime
import copy


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
                dimension2.append(record.copy())
                table.append(copy.deepcopy(dimension2))
                first_entry = False
            else:
                for i in range(len(table)):
                    if table[i][0][3] == pic_source:
                        source_index = i
                        break
                if source_index < 0:
                    dimension2.clear()
                    dimension2.append(record.copy())
                    table.append(copy.deepcopy(dimension2))
                else:
                    tablerec = table[source_index]
                    tablerec.append(record.copy())
                    table[source_index] = tablerec

    return table   

def getpics_around_actual_tstamp(tline_table, act_new_tstamp, nr_before=2, nr_after=2):
    pics_around = []
    picsortlist = []
    for source in tline_table:
        for pic in source:
            picsortlist.append(pic[2])
    picsortlist.sort()
    try:
        index = picsortlist.index(act_new_tstamp)
    except ValueError:
        pics_around = None
    else:
        source_lengts = [len(s) for s in tline_table]
        nrpics = sum(source_lengts)
        if nrpics <= 0:
           pics_around = []
        else:
            #ind_neg = 0 if index - nr_before >= 0 else (index - nr_before) * (-1) #check if and how far index goes negative
            #indexes = [i for i in range(index - nr_before + ind_neg, index + nr_after + ind_neg + 1)]
            #if len(indexes) > nrpics:  #limit pics if not enough in table
            #indexes = indexes[:nrpics]
            ind_neg = 0 if index - nr_before >= 0 else (nr_before - index) #check if and how far indexes go negative
            ind_over = 0 if index + nr_after < nrpics else nrpics -1 -(index + nr_after) #check if and how far exceeding nbr of pics
            indexes = [i for i in range(index - nr_before + ind_neg, index + nr_after + ind_over + 1)]
            
            len_indexes = len(indexes)
            for i in range(0, len_indexes):
                indexes[i] = picsortlist[indexes[i]] #indexes now containes the timestamps
                pics_around.append(None)
            
            for source in tline_table:
                for pic in source:
                    if pic[2] in indexes:
                        i_indexes = indexes.index(pic[2])
                        pics_around[i_indexes] = pic[0] + pic[4]
                        indexes[i_indexes] = 0
                        len_indexes -= 1
                    if len_indexes <= 0:
                        break    
                if len_indexes <= 0:
                    break             
    finally:      
        return pics_around


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


def get_source_index(time_line_table, source):
    index = -1
    for i, sourcesrow in enumerate(time_line_table):
        if sourcesrow[0][3] == source:
            index = i
            break
    return index


def get_picname_index(time_line_table, name, source=None):
    index = -1
    if source is None:
        source = str(name).split('_')[-1]
    src_ind = get_source_index(time_line_table, source)    
    for i in range(len(time_line_table[src_ind])):
        if time_line_table[src_ind][i][0] == name:
            index = i
            break
    return index


def tstamp_to_nice_date(tstamp, factor_pix, tstamp_min):
    n_d = timestamp_to_filenamedatetm((tstamp/factor_pix) + tstamp_min)
    n_d = n_d[6:8] + "/" + n_d[4:6] + "/" + n_d[:4] + "  " + n_d[9:11] + ":" + n_d[11:13] + ":" + n_d[13:]
    return n_d

def calc_text_timeline_item(record):
    if record[1] != record[2]:
        return record[0] + "(" + timestamp_to_filenamedatetm(record[2]) + ")"
    else:
        return record[0]

if __name__ == '__main__': # test
    filedt = "20230325_145622"
    stamp = filenamedatetm_to_timestamp(filedt)
    print(filedt)
    print(stamp)    
    print(timestamp_to_filenamedatetm(stamp))
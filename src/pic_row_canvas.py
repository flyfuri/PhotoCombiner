import tkinter as tk
from PIL import Image, ImageTk
import os
import copy

THUMBNAIL_H = 160
THUMBN_CNR_H = 200

class PicRowCanvas(tk.Canvas):
    

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.image_paths = []  # List to store image paths
        self.photo_images = []  # List to store PhotoImage objects
        self.labels = {}  # Dictionary to store labels
        self.cntr_pic_bigger = None
        self.prev_cntr_pic_small = None
        self.prev_cntr_pic_path = None

    def get_item_width_height(self, item):
        img_x0, img_y0, img_x1, img_y1 = self.bbox(item)
        w = img_x1 - img_x0
        h = img_y1 - img_y0
        return (w,h)
    
    def open_pic_file_to_photo(self, image_path, tmbn_height=100):
        img = Image.open(image_path)
        width, height = img.size
        new_height = tmbn_height
        new_width = int((width / height) * new_height)
        img.thumbnail((new_width, new_height))  # Resize the image to a thumbnail
        return ImageTk.PhotoImage(img)
    
        
    def add_pic_to_row(self, image_path):
        if os.path.exists(image_path):
            photo = self.open_pic_file_to_photo(image_path, THUMBNAIL_H)
            self.image_paths.append(image_path)
            self.photo_images.append(photo)

            position = len(self.labels) * 120 + 10
            image_item = self.create_image(position, 0, anchor=tk.NW, image=photo, tags=image_path)
            text_item = self.create_text(position, THUMBN_CNR_H + 1, text=os.path.basename(image_path), anchor=tk.NW, tags=image_path)
            self.labels[image_path] = (image_item, text_item)

    def delete_pic_from_row(self, image_path):
        if image_path in self.image_paths:
            self.image_paths.remove(image_path)
        if image_path in self.labels:
            image_item, text_item = self.labels.pop(image_path)
            self.delete(image_item)
            self.delete(text_item)


    def update_positions(self, path_centerpic=None):
        i_center = 0
        if path_centerpic in self.image_paths:
            i_center = self.image_paths.index(path_centerpic)
        else:
            i_center = int(len(self.image_paths) / 2)

        centerpos  = int(self.winfo_width()/2)
        pos_x, pos_y = centerpos, 0

        for i in range(i_center, -1, -1):
            items = self.labels[self.image_paths[i]]
            image_width, _ = self.get_item_width_height(items[0])
            text_width, _ = self.get_item_width_height(items[1]) 
            if i == i_center: #center picture
                if path_centerpic != self.prev_cntr_pic_path:
                    if self.prev_cntr_pic_path is not None:
                        if self.prev_cntr_pic_path in self.labels: 
                            prev_items = self.labels[self.prev_cntr_pic_path] #restore previous center pic to small
                            self.itemconfig(prev_items[0], image=self.prev_cntr_pic_small)
                    self.prev_cntr_pic_small = self.itemcget(items[0], 'image') #memorize reference to small pic for restore
                    self.prev_cntr_pic_path = path_centerpic  #memorize path for small pic restore 
                    self.cntr_pic_bigger = self.open_pic_file_to_photo(path_centerpic, THUMBN_CNR_H)
                pos_y = 0
                self.itemconfig(items[0], image=self.cntr_pic_bigger)
                image_width, _ = self.get_item_width_height(items[0])
                pos_x = centerpos - (image_width if image_width > text_width else text_width)/2 
            else:
                pos_y = (THUMBN_CNR_H - THUMBNAIL_H)/2
                pos_x -= (image_width if image_width > text_width else text_width) + 10
            self.coords(items[0], pos_x, pos_y)
            self.coords(items[1], pos_x, THUMBN_CNR_H + 1)

        for i in range(i_center, len(self.image_paths), 1):
            items = self.labels[self.image_paths[i]]
            img_x0, img_y0, img_x1, img_y1 = self.bbox(items[0])
            image_width, _ = self.get_item_width_height(items[0])
            text_width, _ = self.get_item_width_height(items[1]) 
            if i == i_center:
                pos_x = centerpos + (image_width if image_width > text_width else text_width)/2 + 10 
            else:               
                self.coords(items[0], pos_x, pos_y)
                self.coords(items[1], pos_x, THUMBN_CNR_H + 1)
                pos_x += (image_width if image_width > text_width else text_width) + 10
        
            #position = 0
            #for image_path in self.image_paths:
            #    items = self.labels[image_path]
            #    self.coords(items[0], position, 0)
            #    self.coords(items[1], position, THUMBNAIL_H + 1)
            #    image_width = self.bbox(items[0])[2] - self.bbox(items[0])[0]
            #    text_width = self.bbox(items[1])[2] - self.bbox(items[1])[0]
            #    position += (image_width if image_width > text_width else text_width) + 10


    def set_all_pics(self, list_pic_paths, path_centerpic=None):
        i_delete = 0
        for i, picpath in enumerate(list_pic_paths):
            if picpath not in self.image_paths:
                self.add_pic_to_row(picpath)
            tmppcp = self.image_paths.pop(self.image_paths.index(picpath))
            self.image_paths.insert(i, tmppcp)
            i_delete = i + 1
        to_delete = [self.image_paths[i] for i in range(i_delete, len(self.image_paths))]
        for td in to_delete:
            self.delete_pic_from_row(td)               
        self.update_positions(path_centerpic=path_centerpic)



if __name__ == '__main__': # test

    import helperfunctions as hlpfnc
    from tkinter import filedialog

    list_pics = []
    workpath = None
    pic_i = [0]  #must be list to make available in function (quick and dirty just for test)
    root = tk.Tk()
    root.minsize(1900, 300)
    root.geometry('1900x300')
    image_row = PicRowCanvas(root, bg='gray', height=150)
    image_row.pack(fill=tk.BOTH, expand=True)

    def rotate_testpics():
        nbr = 5 if 5 < len(list_pics) -1 else len(list_pics) -1
        if nbr > 1:
            pics_show = list_pics[pic_i[0]:pic_i[0]+nbr]
            index_center = int(nbr/2)
            index_center = index_center if (index_center) % 2 == 0 else index_center + 1
            image_row.set_all_pics(list_pic_paths=[os.path.join(workpath, pic) for pic in pics_show],
                                   path_centerpic=os.path.join(workpath,pics_show[index_center]))
            pic_i[0] += 1
            if pic_i[0] >= len(list_pics)-nbr-1:
                pic_i[0] = 0
            timer = root.after(1000, rotate_testpics)


     # Open a file dialog for opening a file
    workpath = filedialog.askdirectory()
    if workpath is not None:
        timer = root.after(1000, rotate_testpics)
        item_list = os.listdir(workpath)
        list_sourcedir = list(filter(lambda x: os.path.isdir(os.path.join(workpath, x)), item_list))
        list_pics = list(filter(lambda x: hlpfnc.is_pic(x) or hlpfnc.is_video(x), item_list))
        

    root.mainloop()






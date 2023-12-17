import tkinter as tk
from PIL import Image, ImageTk
import os

THUMBNAIL_H = 200

class PicRowCanvas(tk.Canvas):
    

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.image_paths = []  # List to store image paths
        self.photo_images = []  # List to store PhotoImage objects
        self.labels = {}  # Dictionary to store labels

    def add_pic_to_row(self, image_path):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            width, height = img.size
            new_height = THUMBNAIL_H
            new_width = int((width / height) * new_height)
            img.thumbnail((new_width, new_height))  # Resize the image to a thumbnail

            photo = ImageTk.PhotoImage(img)
            self.image_paths.append(image_path)
            self.photo_images.append(photo)

            position = len(self.labels) * 120 + 10
            image_item = self.create_image(position, 0, anchor=tk.NW, image=photo, tags=image_path)
            text_item = self.create_text(position, THUMBNAIL_H + 1, text=os.path.basename(image_path), anchor=tk.NW, tags=image_path)
            self.labels[image_path] = (image_item, text_item)

    def delete_pic_from_row(self, image_path):
        if image_path in self.image_paths:
            self.image_paths.remove(image_path)
        if image_path in self.labels:
            image_item, text_item = self.labels.pop(image_path)
            self.delete(image_item)
            self.delete(text_item)


    def update_positions(self):
        position = 0
        for image_path in self.image_paths:
            items = self.labels[image_path]
            self.coords(items[0], position, 0)
            self.coords(items[1], position, THUMBNAIL_H + 1)
            image_width = self.bbox(items[0])[2] - self.bbox(items[0])[0]
            text_width = self.bbox(items[1])[2] - self.bbox(items[1])[0]
            position += (image_width if image_width > text_width else text_width) + 10


    def set_all_pics(self, list_pic_paths):
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
        self.update_positions()



if __name__ == '__main__': # test

    import helperfunctions as hlpfnc
    from tkinter import filedialog

    list_pics = []
    workpath = None
    pic_i = [0]  #must be list to make available in function (quick and dirty just for test)
    root = tk.Tk()
    root.minsize(1900, 300)
    root.geometry('1900x300')
    image_row = PicRowCanvas(root, bg='white', height=150)
    image_row.pack(fill=tk.BOTH, expand=True)

    def rotate_testpics():
        nbr = 5 if 5 < len(list_pics) -1 else len(list_pics) -1
        if nbr > 1:
            pics_show = list_pics[pic_i[0]:pic_i[0]+nbr]
            image_row.set_all_pics([os.path.join(workpath, pic) for pic in pics_show])
            pic_i[0] += 1
            if pic_i[0] < len(list_pics)-nbr:
                timer = root.after(1000, rotate_testpics)


     # Open a file dialog for opening a file
    workpath = filedialog.askdirectory()
    if workpath is not None:
        timer = root.after(1000, rotate_testpics)
        item_list = os.listdir(workpath)
        list_sourcedir = list(filter(lambda x: os.path.isdir(os.path.join(workpath, x)), item_list))
        list_pics = list(filter(lambda x: hlpfnc.is_pic(x) or hlpfnc.is_video(x), item_list))
        

    root.mainloop()






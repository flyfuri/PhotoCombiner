import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import cv2
import os
import copy
import time
import helperfunctions as hlpfnc

THUMBNAIL_H = 160
THUMBN_CNR_H = 200
VID_PREV_MS = 200

class PicRowCanvas(tk.Canvas):
    

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.image_paths = []  # List to store image paths
        self.photo_images = {}  # Dictionary to store photo images (key = path)
        self.labels = {}  # Dictionary to store labels (key = path)
        self.vidframes = {} # Dictionary to store actual frame on video (key = path)
        self.cntr_pic_bigger = None  #bigger picture in centre
        self.prev_cntr_pic_path = None #memorize which picture is to replace
        self.vid_preview_path = None #picture video preview is running
        self.vid_preview_fps = 0
        self.vid_preview_nbr_frm = 0
        self.vid_preview_interv_frm = 6
        self.vid_preview_capt = None
        self.vid_preview_image = None


    def on_video_prev_timer(self):
        if self.vid_preview_path is not None:
            t_start = time.time()
            self.vidframes[self.vid_preview_path] += self.vid_preview_interv_frm
            if self.vidframes[self.vid_preview_path] >= self.vid_preview_nbr_frm:
                self.vidframes[self.vid_preview_path] = 1
            elif self.vidframes[self.vid_preview_path] <= 0:
                self.vidframes[self.vid_preview_path] = self.vid_preview_nbr_frm - 1   
            
            items = self.labels[self.vid_preview_path]
            
            _, h  = self.get_item_width_height(items[0]) 
            self.vid_preview_image = self.open_pic_file_to_photo(self.vid_preview_path, h)
            self.itemconfigure(items[0], image=self.vid_preview_image) 
            self.photo_images[self.vid_preview_path] = self.vid_preview_image
            t_used = (time.time() - t_start) * 1000
            t_next = VID_PREV_MS - t_used
            t_next = t_next if t_next >= 2 else 2
            self.after(int(t_next), self.on_video_prev_timer)
        elif self.act_prev_capt is not None:
            self.act_prev_capt.release()
            self.act_prev_capt = None


    def on_pic_mouse_down(self, event, reverse=False):
        path = event.widget.gettags(tk.CURRENT)[0]
        if hlpfnc.is_video(path):
            self.vid_preview_path = path
            self.act_prev_capt = cv2.VideoCapture(path)
            self.vid_preview_nbr_frm = self.act_prev_capt.get(cv2.CAP_PROP_FRAME_COUNT)
            self.vid_preview_fps = self.act_prev_capt.get(cv2.CAP_PROP_FPS)
            if not reverse:
                self.vid_preview_interv_frm = int(self.vid_preview_fps/(1000/VID_PREV_MS))
            else:
                self.vid_preview_interv_frm = int(self.vid_preview_fps/(-1000/VID_PREV_MS))

            self.after(1, self.on_video_prev_timer)

    def on_pic_mouse_up(self, event):
        self.vid_preview_path = None
        if self.act_prev_capt is not None:
            self.act_prev_capt.release()
            self.act_prev_capt = None
     

    def get_item_width_height(self, item):
        img_x0, img_y0, img_x1, img_y1 = self.bbox(item)
        w = img_x1 - img_x0
        h = img_y1 - img_y0
        return (w,h)
    
    def draw_default_image(self, width=200, height=100):
        default_image = Image.new("RGB", (min(width,20), min(height, 20)), 'silver')
        draw = ImageDraw.Draw(default_image)
        draw.rounded_rectangle((5,5,width-5,height-5), fill='blue')
        return default_image

    def open_pic_file_to_photo(self, image_path, tmbn_height=100):
        try:
            if hlpfnc.is_pic(os.path.basename(image_path)):
                img = Image.open(image_path)
            elif hlpfnc.is_video(os.path.basename(image_path)):
                capt = cv2.VideoCapture(image_path)
                try:
                    framepos = self.vidframes[image_path]
                except:
                    vid_nb_frames = capt.get(cv2.CAP_PROP_FRAME_COUNT)
                    framepos = int(vid_nb_frames/2)
                    self.vidframes[image_path] = framepos
                
                capt.set(cv2.CAP_PROP_POS_FRAMES, framepos)
                readOK, bgr_frame = capt.read()
                capt.release()
                if readOK:
                    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)           
                    img = Image.fromarray(rgb_frame)# Convert the frame to a Pillow Image
                else:
                    raise Exception    
            else: 
                raise Exception
        except Exception as e:        
            #print(str(e))
            img = self.draw_default_image(200,100)

        width, height = img.size
        new_height = tmbn_height
        new_width = int((width / height) * new_height)
        img.thumbnail((new_width, new_height))  # Resize the image to a thumbnail
        return ImageTk.PhotoImage(img)
    
        
    def add_pic_to_row(self, image_path, size_h):
        if os.path.exists(image_path):
            self.photo_images[image_path] = self.open_pic_file_to_photo(image_path, size_h)
            self.image_paths.append(image_path)

            position = len(self.labels) * 120 + 10
            image_item = self.create_image(position, 0, anchor=tk.NW, image=self.photo_images[image_path], tags=[image_path])
            #self.tag_bind(image_path, "<Enter>", self.on_mouse_enter_pic)  event did not trigger reliably
            #self.tag_bind(image_path,"<Leave>", self.on_mouse_leave_pic)   event did not trigger reliably
            self.tag_bind(image_path, '<ButtonPress-1>', lambda event, reverse=False : self.on_pic_mouse_down(event, reverse))
            self.tag_bind(image_path,'<ButtonRelease-1>', self.on_pic_mouse_up)
            self.tag_bind(image_path, '<ButtonPress-3>', lambda event, reverse=True : self.on_pic_mouse_down(event, reverse))
            self.tag_bind(image_path,'<ButtonRelease-3>', self.on_pic_mouse_up)
            text_item = self.create_text(position, THUMBN_CNR_H + 1, text=os.path.basename(image_path), anchor=tk.NW, tags=[image_path])
            self.labels[image_path] = (image_item, text_item)


    def resize_height_pic_in_row(self, image_path, size_h):
        if os.path.exists(image_path):
            self.photo_images[image_path] = self.open_pic_file_to_photo(image_path, size_h)
            items = self.labels[image_path] #restore previous center pic to small
            self.itemconfig(items[0], image=self.photo_images[image_path])


    def delete_pic_from_row(self, image_path):
        if image_path in self.photo_images:
            self.photo_images.pop(image_path)
        if image_path in self.labels:
            image_item, text_item = self.labels.pop(image_path)
            self.delete(image_item)
            self.delete(text_item)
        if image_path in self.image_paths:
            self.image_paths.remove(image_path)


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
                pos_y = 0
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


    def set_all_pics(self, list_pic_paths=[], path_centerpic=None):
        i_delete = 0
        for i, picpath in enumerate(list_pic_paths):
            if picpath not in self.image_paths:
                size_h = THUMBN_CNR_H if picpath == path_centerpic else THUMBNAIL_H
                self.add_pic_to_row(picpath, size_h)
            elif path_centerpic != self.prev_cntr_pic_path: #if centerpic has changed since last time
                if picpath == path_centerpic:
                    self.resize_height_pic_in_row(picpath, THUMBN_CNR_H)
                elif picpath == self.prev_cntr_pic_path:   
                    self.resize_height_pic_in_row(picpath, THUMBNAIL_H)

            tmppcp = self.image_paths.pop(self.image_paths.index(picpath)) #extract to put at new index
            self.image_paths.insert(i, tmppcp) #new index as in list_pic_path
            i_delete = i + 1
        self.prev_cntr_pic_path = path_centerpic
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






# graphical elements
        self.rootW = None
        self.frame1 = None
        self.frame2 = None
        self.canvas_Tline = None
        self.timescroll = None
        self.cursorText = None
        self.btn_workpath = None
        self.btn_merge = None
        self.btn_rename = None
        self.create_window()

    def create_window(self):
        self.rootW = tk.Tk()
        self.rootW.title("PhotoCombiner")
        self.rootW.resizable(width=True, height=True)
        self.rootW.minsize(800, 600)
        self.rootW.geometry('800x600')
        self.rootW.state('zoomed')

        # frame 1 working path
        self.frame1 = Frame(self.rootW)
        self.frame1.pack()
        lbl_workpath = Label(self.frame1, text="working path(folder):")
        self.var_workpathvalue = tk.StringVar()
        lbl_workpathvalue = Label(self.frame1, textvariable=self.var_workpathvalue)
        btn_workpath = tk.Button(self.frame1, text="...",command=self.on_click_btn_workpath)
        lbl_workpath.pack(side='left' )
        lbl_workpathvalue.pack(side='left')
        btn_workpath.pack(side='left')
        btn_merge = tk.Button(self.frame1, text="merge from sources",command=self.on_click_btn_merge, state=tk.DISABLED)
        btn_merge.pack(side='left')
        btn_rename = tk.Button(self.frame1, text="rename moved pics",command=self.on_click_btn_rename, state=tk.DISABLED)
        btn_rename.pack(side='left')

        # frame 2 Canvas
        self.frame2 = Frame(self.rootW)
        self.frame2.pack(side='bottom', expand=True, fill='x')
        self.canvas_Tline = tk.Canvas(self.frame2, bg='white', scrollregion=(0,0,CANVAS_WIDTH, CANVAS_HEIGHT))
        self.timescroll = tk.Scrollbar(self.frame2, orient='horizontal', command=self.canvas_Tline.xview)
        self.timescroll.pack(side='bottom', fill='x')
        self.canvas_Tline.pack(side='bottom', expand=False, fill='x')
        self.canvas_Tline.configure(xscrollcommand=self.timescroll.set)
        self.cursorText = self.canvas_Tline.create_text(1, 1, fill='black', text='')
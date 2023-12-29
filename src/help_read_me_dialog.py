import tkinter as tk
from PIL import Image
from tkinterweb import HtmlFrame
import markdown2
import re
import os
import sys

class ReadMeMessageBox(tk.Toplevel):
    def __init__(self, parent, file_path=None, title="help", *args, **kwargs ):
        super().__init__(parent, *args, **kwargs)

        self.current_work_directory = os.path.split(sys.argv[0])[0]  
        if file_path is not None and os.path.exists(file_path):
            self.file_path = file_path 
        else:
            self.file_path = os.path.join(self.current_work_directory, 'readme.md')
        self.title(title)
            
    def close_dialog(self):
        self.destroy()

    def show_markdown_readme(self):
        while not os.path.exists(self.file_path):
            path, file = os.path.split(self.file_path)
            path_shortened, part_cut = os.path.split(path)
            if path_shortened == '' or part_cut == '':  #end reached
                break
            self.file_path = os.path.join(os.path.split(path)[0], file)
                
                
        if not os.path.exists(self.file_path):
            html_content = '<h2>readme.md file could not be found.<p> Please go to https://github.com/flyfuri/PhotoCombiner#photocombiner</p></h2>'
        else:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            html_content = str(markdown2.markdown(content))

        html_content = html_content.replace("<img src=\"" , "<img src=\"file:///D:/GitHubReposVSCode/PhotoSort")

        #limit pic size  
        matches = re.findall(r'(<img src=\".*?\.jpg|gif|bmp|png)', html_content, re.IGNORECASE)
        if matches:
            for i, match in enumerate(matches):
                with Image.open(match[len("<img src=\"file:///") : ]) as img:
                    width, _ = img.size
                    to_replace_with = "\" style=\"width: " + str(min(1000, width)) + "px; height: auto;"
                    html_content = html_content.replace("raw=true", to_replace_with, i+1)

        #self.protocol("WM_DELETE_WINDOW", self.close_dialog)
        self.frame = HtmlFrame(self) 
        self.frame.load_html(html_content) 
        self.frame.pack(fill="both", expand=True) 
       
        # Add a Button to close the dialog
        close_button = tk.Button(self, text="Close", height=2,  command=self.close_dialog)
        close_button.pack(padx=10, pady=10)


if __name__ == '__main__': # test

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    current_file_directory = sys.argv[0]
    file_path = os.path.join(current_file_directory, 'readme.md')
    dialog = ReadMeMessageBox(parent=root, file_path=file_path, title="testhelp")
    dialog.show_markdown_readme()

    root.mainloop()
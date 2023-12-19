import tkinter as tk
import ctypes
from typing import List
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay
from PIL import Image, ImageTk
import cv2
import threading

class TkOverlay(BaseOverlay):

    dpi_scaling = 1    
    lock = threading.Lock()
    
    def __init__(self, method : CaptureMethodBase):
        self.method = method
        self.uiDict = {}
        root = tk.Tk()
        self.root = root
        self.init_window()
        self.init_canvas()
        method.add_window_change_listener(self)
    
    def init_window(self):
        self.root.title("TkOverlay")        
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', self.root['bg'])
        self.root.wm_attributes("-topmost", True)    
    
    def init_canvas(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)        
        self.canvas.place(relwidth=1, relheight=1)
        
    def draw_boxes(self, key:str, boxes:List[Box], outline:str):  
        self.root.after(0, lambda: self.tk_draw_boxes(key, boxes, outline))     
        
    def tk_draw_boxes(self, key:str, boxes:List[Box], outline:str):
        if key not in self.uiDict:
            self.uiDict[key] = []
        for ui in self.uiDict[key]:
            self.canvas.delete(ui)
        for box in boxes:
            print(f"draw box {box}")
            self.uiDict[key].append(self.canvas.create_rectangle(box.x/self.dpi_scaling, box.y/self.dpi_scaling, (box.x + box.width)/self.dpi_scaling, (box.y + box.height)/self.dpi_scaling, outline=outline))
            self.uiDict[key].append(self.canvas.create_text(box.x/self.dpi_scaling, (box.y+box.width)/self.dpi_scaling, anchor="nw", fill=outline, text=f"{key}_{round(box.confidence*100)}", font=("Arial", 20)))

    def window_changed(self, visible, x, y, border, title_height,window_width, window_height, scaling):
        self.dpi_scaling = scaling
        print(f"TkOverlay window_changed {round(window_width/self.dpi_scaling)}x{round(window_height/self.dpi_scaling)}+{round(x)}+{round((y+title_height/self.dpi_scaling))}")
        self.root.geometry(f"{round(window_width/self.dpi_scaling)}x{round(window_height/self.dpi_scaling)}+{round(x+border/self.dpi_scaling)}+{round((y+title_height/self.dpi_scaling))}")
        if visible:
            self.root.deiconify()
        else:
            self.root.withdraw()

    def start(self):
        self.root.mainloop()

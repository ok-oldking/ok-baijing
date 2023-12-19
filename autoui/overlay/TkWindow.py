import tkinter as tk
from typing import List
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.Box import Box
from autoui.overlay.TkOverlay import TkOverlay
from PIL import Image, ImageTk
import threading
import cv2

# for the purpose of finding latency
class TkWindow(TkOverlay):

    dpi_scaling = 1    
    image_on_canvas = None
    tk_img = None
    pil_img = None

    def init_window(self):
        self.root.title("TkWindow")  
        self.root.after(100, self.draw)

    def draw(self):
        self.lock.acquire()
        if self.pil_img is None:
            self.lock.release() 
            return
        self.pil_img.thumbnail((self.root.winfo_width(), self.root.winfo_height()))
        self.tk_img = ImageTk.PhotoImage(image=self.pil_img)
        self.pil_image = None 
        self.lock.release()            
        if self.image_on_canvas is None:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        else:
            self.canvas.itemconfig(self.image_on_canvas, image=self.tk_img)    
        self.root.after(10, self.draw)

    def draw_image(self, image):              
        self.lock.acquire()
        self.pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).copy()
        self.lock.release()
        # 
         
             
    def window_changed(self, visible, x, y, border, title_height,window_width, window_height, scaling):
        self.dpi_scaling = scaling
        print(f"TkWindow window_changed {round(window_width/self.dpi_scaling)}x{round(window_height/self.dpi_scaling)}+{round(x)}+{round((y+title_height/self.dpi_scaling))}")
        self.root.geometry(f"{round(window_width/self.dpi_scaling)}x{round(window_height/self.dpi_scaling)}")
   

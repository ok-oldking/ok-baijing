import tkinter as tk
import ctypes
from typing import List
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay

class TkOverlay(BaseOverlay):

    dpi_scaling = 1
    
    def __init__(self, method : CaptureMethodBase):

        # Create a top-level window
        # ctypes.windll.shcore.SetProcessDpiAwareness(0) 
        # ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.method = method
        self.uiDict = {}
        root = tk.Tk()
        root.title("TkOverlay")

        # Set the window size and position to match your game window

        # Make the window borderless and transparent

        # Example drawing: a red rectangle
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        root.overrideredirect(True)
        root.attributes('-transparentcolor', root['bg'])
        # Keep the window always on top
        root.wm_attributes("-topmost", True) 
        # root.configure(bg="lightblue")       
        self.root = root
        
        method.add_window_change_listener(self)
        
    def draw_boxes(self, key:str, boxes:List[Box], outline:str):       
        if key not in self.uiDict:
            self.uiDict[key] = []
        for ui in self.uiDict[key]:
            # print(f"delete {ui}")
            self.canvas.delete(ui)
        for box in boxes:
            print(f"draw box {box}")
            self.uiDict[key].append(self.canvas.create_rectangle(box.x/self.dpi_scaling, box.y/self.dpi_scaling, (box.x + box.width)/self.dpi_scaling, (box.y + box.height)/self.dpi_scaling, outline=outline))
            self.uiDict[key].append(self.canvas.create_text(box.x/self.dpi_scaling, (box.y+box.width)/self.dpi_scaling, anchor="nw", fill=outline, text=key, font=("Arial", 40)))

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

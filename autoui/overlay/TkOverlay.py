import threading
import time  # Import time module to track update times
import tkinter as tk
from typing import List

from autoui.capture.HwndWindow import HwndWindow
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay


class TkOverlay(BaseOverlay):
    dpi_scaling = 1
    lock = threading.Lock()

    def __init__(self, window: HwndWindow, exit_event: threading.Event):
        super().__init__()
        self.canvas = None
        self.window = window
        self.uiDict = {}
        self.textDict = {}
        root = tk.Tk()
        self.root = root
        self.init_window()
        self.init_canvas()
        self.exit_event = exit_event
        self.time_to_expire = 0.5
        self.root.after(100, self.remove_expired_ui)
        window.add_window_change_listener(self)

    def init_window(self):
        self.root.title("TkOverlay")
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', self.root['bg'])
        self.root.wm_attributes("-topmost", True)

    def init_canvas(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.place(relwidth=1, relheight=1)

    def draw_boxes(self, key: str, boxes: List[Box], outline: str):
        if self.exit_event and self.exit_event.is_set():
            return
        self.root.after(0, lambda: self.tk_draw_boxes(key, boxes, outline))

    def draw_text(self, key: str, x, y, text: str):
        if self.exit_event and self.exit_event.is_set():
            return
        self.root.after(0, lambda: self.do_draw_text(key, x, y, text))

    def do_draw_text(self, key: str, x, y, text: str):
        """Draw or update text on the screen at a given position."""
        with self.lock:  # Use the lock to ensure thread safety
            # Convert relative position to actual position based on canvas size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            abs_x, abs_y = x * canvas_width, y * canvas_height

            # Check if text (and its position) needs to be updated or created
            if key in self.textDict:
                text_id, existing_text, existing_position = self.textDict[key]
                # Update text and/or position if they have changed
                if text != existing_text or (abs_x, abs_y) != existing_position:
                    self.canvas.itemconfig(text_id, text=text)
                    self.canvas.coords(text_id, abs_x, abs_y)
                    # Update stored text and position
                    self.textDict[key] = (text_id, text, (abs_x, abs_y))
            else:
                # Create new text element
                text_id = self.canvas.create_text(abs_x, abs_y, anchor="nw", fill="red", text=text,
                                                  font=("Arial", 20))
                # Store text ID, content, and position
                self.textDict[key] = (text_id, text, (abs_x, abs_y))

    def tk_draw_boxes(self, key: str, boxes: List[Box], outline: str):
        current_time = time.time()  # Get the current time
        with self.lock:  # Use the lock to ensure thread safety
            # Check and remove old UI elements
            # self.remove_expired_ui(current_time)

            # delete old
            if key in self.uiDict:
                for ui in self.uiDict[key]:
                    self.canvas.delete(ui[0])

            self.uiDict[key] = []

            # Draw new boxes and record their creation time
            for box in boxes:
                x = self.window.frame_ratio(box.x)
                y = self.window.frame_ratio(box.y)
                width = self.window.frame_ratio(box.width)
                height = self.window.frame_ratio(box.height)
                rect = self.canvas.create_rectangle(
                    x / self.dpi_scaling, y / self.dpi_scaling,
                    (x + width) / self.dpi_scaling,
                    (y + height) / self.dpi_scaling,
                    outline=outline)
                text = self.canvas.create_text(
                    x / self.dpi_scaling, (y + width) / self.dpi_scaling, anchor="nw",
                    fill=outline, text=f"{key}_{round(box.confidence * 100)}", font=("Arial", 20))
                # Append the UI element and the current time to the uiDict
                self.uiDict[key].append([rect, current_time])
                self.uiDict[key].append([text, current_time])

    def remove_expired_ui(self):
        if self.exit_event.is_set():
            print("TKOverlay: Exit event")
            self.root.destroy()
            return
        current_time = time.time()
        for key in list(self.uiDict.keys()):  # Use list to iterate over a copy of the keys
            old_uis = [ui for ui, update_time in self.uiDict[key] if
                       current_time - update_time >= self.time_to_expire]

            # Remove old UI elements
            for ui in old_uis:
                self.canvas.delete(ui)

            # Filter out the old UI elements and keep the remaining ones
            remaining_uis = [ui for ui in self.uiDict[key] if
                             current_time - ui[1] < self.time_to_expire]

            # Update the dictionary based on whether there are any remaining UIs
            if remaining_uis:
                self.uiDict[key] = remaining_uis
            else:
                del self.uiDict[key]
        self.root.after(200, self.remove_expired_ui)

    def window_changed(self, visible, x, y, border, title_height, window_width, window_height, scaling):
        self.dpi_scaling = scaling
        print(
            f"TkOverlay window_changed {round(window_width / self.dpi_scaling)}x{round(window_height / self.dpi_scaling)}+{round(x)}+{round((y + title_height / self.dpi_scaling))}")
        self.root.geometry(
            f"{round(window_width / self.dpi_scaling)}x{round(window_height / self.dpi_scaling)}+{round(x + border / self.dpi_scaling)}+{round((y + title_height / self.dpi_scaling))}")
        if visible:
            self.root.deiconify()
        else:
            self.root.withdraw()

    def start(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            # Handle what happens after Ctrl+C is presse
            print("TkinterCaught KeyboardInterrupt, exiting...")
            if self.exit_event:
                self.exit_event.set()
            self.root.destroy()

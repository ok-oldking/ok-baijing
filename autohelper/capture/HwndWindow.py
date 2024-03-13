# original https://github.com/dantmnf & https://github.com/hakaboom/winAuto
import threading

from typing_extensions import override
from win32 import win32gui

from autohelper.capture.windows.window import is_foreground_window, get_window_bounds
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class HwndWindow:
    visible = True
    x = 0
    y = 0
    width = 0
    height = 0
    title_height = 0
    border = 0
    scaling = 1
    top_cut = 0
    right_cut = 0
    bottom_cut = 0
    left_cut = 0
    window_change_listeners = []
    frame_aspect_ratio = 0
    hwnd = None
    frame_width = 0
    frame_height = 0

    def __init__(self, title="", exit_event=threading.Event(), frame_width=0, frame_height=0):
        super().__init__()
        self.title = title
        self.visible = False
        self.update_frame_size(frame_width, frame_height)
        self.hwnd = win32gui.FindWindow(None, title)
        if not self.hwnd:
            raise Exception(f"window {title} not found")

        self.thread = threading.Thread(target=self.update_window_size)
        self.exit_event = exit_event
        self.do_update_window_size()
        self.thread.start()

    @override
    def close(self):
        self.exit_event.set()

    def update_frame_size(self, width, height):
        if width != self.frame_width or height != self.frame_height:
            self.frame_width = width
            self.frame_height = height
            if width > 0 and height > 0:
                self.frame_aspect_ratio = width / height
                print(f"HwndWindow: frame ratio:{self.frame_aspect_ratio} width: {width}, height: {height}")

    def add_window_change_listener(self, listener):
        self.window_change_listeners.append(listener)
        listener.window_changed(self.visible, self.x, self.y, self.border, self.title_height, self.width, self.height,
                                self.scaling)

    def update_window_size(self):
        while not self.exit_event.is_set():
            self.do_update_window_size()
            self.exit_event.wait(0.1)

    def get_abs_cords(self, x, y):
        return int(self.x + (self.border + x) / self.scaling), int(self.y + (y + self.title_height) / self.scaling)

    def do_update_window_size(self):
        x, y, border, title_height, window_width, window_height, scaling = get_window_bounds(self.hwnd)
        if self.frame_aspect_ratio != 0:
            window_ratio = window_width / window_height
            # print(f"window_ratio: {window_ratio} frame_aspect_ratio: {self.frame_aspect_ratio}")
            if window_ratio < self.frame_aspect_ratio:
                cropped_window_height = int(window_width / self.frame_aspect_ratio)
                title_height += window_height - cropped_window_height
                window_height = cropped_window_height
        visible = is_foreground_window(self.hwnd)
        if self.title_height != title_height or self.border != border or visible != self.visible or self.x != x or self.y != y or self.width != window_width or self.height != window_height:
            logger.debug(f"update_window_size: {x} {y} {title_height} {border} {window_width} {window_height}")
            self.visible = visible
            self.x = x  # border_width
            self.y = y  # titlebar_with_border_height
            self.title_height = title_height
            self.border = border
            self.width = window_width  # client_width
            self.height = window_height  # client_height - border_width * 2
            self.scaling = scaling
            for listener in self.window_change_listeners:
                listener.window_changed(visible, x, y, border, title_height, window_width, window_height, scaling)

    def frame_ratio(self, size):
        if self.frame_width > 0 and self.width > 0:
            return int(size / self.frame_width * self.width)
        else:
            return size

import ctypes
import sys
import time

import pydirectinput

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay


class Win32Interaction:

    def __init__(self, capture: BaseCaptureMethod, overlay: BaseOverlay = None):
        self.overlay = overlay
        self.capture = capture
        self.post = ctypes.windll.user32.PostMessageW
        if not is_admin():
            print(f"You must be an admin to use Win32Interaction", file=sys.stderr)

    def send_key(self, key, down_time=0.02):
        if not self.capture.bring_to_front():
            return
        pydirectinput.keyDown(key)
        time.sleep(down_time)
        pydirectinput.keyUp(key)

    def left_click_relative(self, x, y):
        self.left_click(int(self.capture.width * x), int(self.capture.height * y))

    def left_click_box(self, box: Box):
        x, y = box.center_with_variance()
        self.left_click(x, y)

    def left_click(self, x=-1, y=-1):
        if not self.capture.bring_to_front():
            return
        # Convert the x, y position to lParam
        # lParam = win32api.MAKELONG(x, y)
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            print(f"Win32Interaction: left_click {x, y}")
            pydirectinput.moveTo(x, y)
        pydirectinput.click()

        # Send the mouse down and up messages
        # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        # time.sleep(down_time)
        # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)


def is_admin():
    try:
        # Only Windows users with admin privileges can read the C drive directly
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

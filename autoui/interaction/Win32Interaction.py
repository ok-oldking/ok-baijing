import ctypes
import time

import pydirectinput

from autoui.capture.CaptureMethodBase import CaptureMethodBase
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay


class Win32Interaction:

    def __init__(self, capture: CaptureMethodBase, overlay: BaseOverlay = None):
        self.overlay = overlay
        self.capture = capture
        self.post = ctypes.windll.user32.PostMessageW

    def send_key(self, key, down_time=0.02):
        if not self.capture.visible:
            return
        pydirectinput.keyDown(key)
        time.sleep(down_time)
        pydirectinput.keyUp(key)
        # win32api.PostMessage(self.hwnd, win32con.WM_CHAR, key, 0)
        # vk_code = self.get_virtual_keycode(key)
        # scan_code = self.MapVirtualKeyW(vk_code, 0)
        # wparam = vk_code
        # lparam = (scan_code << 16) | 1
        # lparam2 = (scan_code << 16) | 0XC0000001
        # self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYDOWN, wparam, lparam)
        # time.sleep(0.05)
        # self.PostMessageW(static_lib.HANDLEOBJ.get_handle(), self.WM_KEYUP, wparam, lparam2)

    def left_click_box(self, box: Box):
        x, y = box.center_with_variance()
        self.left_click(x, y)

    def left_click(self, x=-1, y=-1):
        if not self.capture.visible:
            return
        # Convert the x, y position to lParam
        # lParam = win32api.MAKELONG(x, y)
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            pydirectinput.moveTo(x, y)
        pydirectinput.click()

        # Send the mouse down and up messages
        # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        # time.sleep(down_time)
        # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

import ctypes
import sys
import time

import pydirectinput

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod
from autoui.interaction.BaseInteraction import BaseInteraction


class Win32Interaction(BaseInteraction):

    def __init__(self, capture: BaseCaptureMethod):
        super().__init__(capture)
        self.post = ctypes.windll.user32.PostMessageW
        if not is_admin():
            print(f"You must be an admin to use Win32Interaction", file=sys.stderr)

    def send_key(self, key, down_time=0.02):
        if not self.capture.clickable():
            return
        pydirectinput.keyDown(key)
        time.sleep(down_time)
        pydirectinput.keyUp(key)

    def click(self, x=-1, y=-1):
        super().click(x, y)
        if not self.capture.clickable():
            print(f"Win32Interaction:not clickable")
            return
        # Convert the x, y position to lParam
        # lParam = win32api.MAKELONG(x, y)
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            print(f"Win32Interaction: left_click {x, y}")
            pydirectinput.moveTo(x, y)
        pydirectinput.click()


def is_admin():
    try:
        # Only Windows users with admin privileges can read the C drive directly
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

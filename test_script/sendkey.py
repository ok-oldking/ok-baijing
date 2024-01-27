import string
import time
from ctypes import windll
from ctypes.wintypes import HWND

import pygetwindow as gw
import win32con
import win32gui

PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101

# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VkCode = {
    "back": 0x08,
    "tab": 0x09,
    "return": 0x0D,
    "shift": 0x10,
    "control": 0x11,
    "menu": 0x12,
    "pause": 0x13,
    "capital": 0x14,
    "escape": 0x1B,
    "space": 0x20,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "print": 0x2A,
    "snapshot": 0x2C,
    "insert": 0x2D,
    "delete": 0x2E,
    "lwin": 0x5B,
    "rwin": 0x5C,
    "numpad0": 0x60,
    "numpad1": 0x61,
    "numpad2": 0x62,
    "numpad3": 0x63,
    "numpad4": 0x64,
    "numpad5": 0x65,
    "numpad6": 0x66,
    "numpad7": 0x67,
    "numpad8": 0x68,
    "numpad9": 0x69,
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "numlock": 0x90,
    "scroll": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lmenu": 0xA4,
    "rmenu": 0XA5
}


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]


def key_down(handle: HWND, key: str):
    """按下指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)


def key_up(handle: HWND, key: str):
    """放开指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)


def bring_to_front(hwnd):
    # Restore the window if it's minimized
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # Bring the window to the front
    win32gui.SetForegroundWindow(hwnd)


def get_foreground_window():
    return win32gui.GetForegroundWindow()
    # return ctypes.windll.user32.GetForegroundWindow()


if __name__ == "__main__":
    # 需要和目标窗口同一权限，游戏窗口通常是管理员权限
    import sys

    if not windll.shell32.IsUserAnAdmin():
        # 不是管理员就提权
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)

    handle = gw.getWindowsWithTitle("Genshin Impact")[0]
    # handle = gw.getWindowsWithTitle("少女前线2：追放")[1]
    fg = gw.getActiveWindow()
    print(f"handle {handle} fg: {fg}")
    time.sleep(3)
    # 控制角色向前移动两秒
    handle.activate()
    # bring_to_front(handle)
    key_down(handle._hWnd, 'b')
    time.sleep(0.1)
    key_up(handle._hWnd, 'b')
    time.sleep(1)
    # bring_to_front(fg)
    print(f"fg.title {fg.title}")
    gw.getWindowsWithTitle(fg.title)[0].show()
    time.sleep(1)

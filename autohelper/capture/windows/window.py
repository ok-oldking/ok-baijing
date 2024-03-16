import ctypes
import ctypes.wintypes
from typing import Any

import win32gui

user32 = ctypes.WinDLL('user32', use_last_error=True)

DWMWA_EXTENDED_FRAME_BOUNDS = 9


def is_window_minimized(hWnd):
    return user32.IsIconic(hWnd) != 0


def get_window_bounds(hwnd) -> tuple[Any, Any, int, int | Any, int, int, float | Any]:
    extended_frame_bounds = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        hwnd,
        DWMWA_EXTENDED_FRAME_BOUNDS,
        ctypes.byref(extended_frame_bounds),
        ctypes.sizeof(extended_frame_bounds),
    )
    scaling = user32.GetDpiForWindow(hwnd) / 96
    window_rect = win32gui.GetWindowRect(hwnd)
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    _, _, client_width, client_height = win32gui.GetClientRect(hwnd)
    # print(f"get_window_bounds: scaling:{scaling},window_rect:{window_rect}, client:({client_x},{client_y},{client_width},{client_height}))")
    # window_left_bounds = extended_frame_bounds.left - window_rect[0]
    # window_top_bounds = extended_frame_bounds.top - window_rect[1]
    client_width = int(client_width * scaling)
    client_height = int(client_height * scaling)
    window_width = extended_frame_bounds.right - extended_frame_bounds.left
    window_height = extended_frame_bounds.bottom - extended_frame_bounds.top
    # print(f"window_width:{window_width} client_width:{client_width}")
    border = int((window_width - client_width) / 2)
    title = window_height - client_height - border
    # print(f"{border}, {title}, {client_width}, {client_height}")
    return window_rect[0], window_rect[1], border, title, client_width, client_height, scaling


def is_foreground_window(hwnd):
    return win32gui.IsWindowVisible(hwnd) and win32gui.GetForegroundWindow() == hwnd

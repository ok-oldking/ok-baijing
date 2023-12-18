import ctypes
import ctypes.wintypes
import win32gui
import win32con
user32 = ctypes.WinDLL('user32', use_last_error=True)

DWMWA_EXTENDED_FRAME_BOUNDS = 9

def is_window_minimized(hWnd):
    return user32.IsIconic(hWnd) != 0

def get_window_bounds(hwnd, top_cut = 0,bottom_cut = 0,left_cut = 0,right_cut = 0) -> tuple[int, int, int, int, int, int]:
        extended_frame_bounds = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(extended_frame_bounds),
            ctypes.sizeof(extended_frame_bounds),
        )
        scaling = user32.GetDpiForWindow(hwnd)/96   
        window_rect = win32gui.GetWindowRect(hwnd)
        window_width = window_rect[2] - window_rect[0]
        window_height = window_rect[3] - window_rect[1]
        _, _, client_width, client_height = win32gui.GetClientRect(hwnd)
        #print(f"get_window_bounds: scaling:{scaling},window_rect:{window_rect}, client:({client_x},{client_y},{client_width},{client_height}))")
        # window_left_bounds = extended_frame_bounds.left - window_rect[0]
        # window_top_bounds = extended_frame_bounds.top - window_rect[1]
        client_width = int(client_width * scaling)
        client_height = int(client_height * scaling)
        window_width = extended_frame_bounds.right - extended_frame_bounds.left
        window_height = extended_frame_bounds.bottom - extended_frame_bounds.top
        #print(f"window_width:{window_width} client_width:{client_width}")
        border = int((window_width - client_width) / 2)
        title = window_height - client_height - border
        #print(f"{border}, {title}, {client_width}, {client_height}")
        client_height = int(client_height - client_height * bottom_cut)
        return window_rect[0], window_rect[1], border, title, client_width, client_height

def is_window_behind(hwnd):
    # Get the first window in the Z-order
    top_window = win32gui.GetForegroundWindow()

    # Traverse the Z-order to check if our window is behind others
    while top_window:
        # If we find our window, it's not behind others
        if top_window == hwnd:
            return False

        # Get the next window in the Z-order
        top_window = win32gui.GetWindow(top_window, win32con.GW_HWNDNEXT)

    # If we didn't find our window, it's behind others or not visible
    return True
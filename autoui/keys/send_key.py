import win32gui
import win32api
import win32con

def send_key(hwnd, key):
    # Post a WM_KEYDOWN and WM_KEYUP message to the window
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)

# Example usage
# hwnd = # Your target window's HWND
# key = win32con.VK_A  # Virtual key code for 'A'

# send_key(hwnd, key)

# Function to find a window by its title
def find_window(title):
    return win32gui.FindWindow(None, title)

# Find the window
hwnd = find_window("原神")

# Check if a valid window handle was found
if hwnd != 0:
    send_key(hwnd, win32con.VK_F1)
else:
    print("Window not found!")
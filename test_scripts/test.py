import pygetwindow as gw
import pyautogui
import time
from PIL import Image

def capture_window(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]  # Get the first window with the given title
        if window is not None:
            window.activate()  # Focus the window
            x, y, width, height = window.left, window.top, window.width, window.height
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            return screenshot
        else:
            print("Window not found")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def print_all_windows_info(title):
    windows = gw.getAllWindows()
    for win in windows:
        if win.title == title:
            print(f"Title: {win.title}")
            print(f"\tHandle: {win._hWnd}")
            print(f"\tWidth: {win.width}, Height: {win.height}")
            print(f"\tLeft: {win.left}, Top: {win.top}")
            print(f"\tIs Visible: {win.visible}")
            print()

def main():
    WINDOW_TITLE = "原神"  # Replace with the title of the window you want to capture
    print_all_windows_info(WINDOW_TITLE)
    INTERVAL = 10  # Save a frame every 10 seconds

    while True:
        frame = capture_window(WINDOW_TITLE)
        if frame:
            frame.save("latest_frame.jpg")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

#original https://github.com/Toufool/AutoSplit/blob/master/src/capture_method/WindowsGraphicsCaptureMethod.py
import asyncio
from typing import TYPE_CHECKING, cast
import threading
import win32api
import numpy as np
from cv2.typing import MatLike
from typing_extensions import override
from win32 import win32gui
from math import ceil
from winsdk.windows.graphics import SizeInt32
from winsdk.windows.graphics.capture import Direct3D11CaptureFramePool, GraphicsCaptureSession
from winsdk.windows.graphics.capture.interop import create_for_window
from winsdk.windows.graphics.directx import DirectXPixelFormat
from winsdk.windows.graphics.imaging import BitmapBufferAccessMode, SoftwareBitmap

from autoui.capture.window import is_foreground_window, get_window_bounds
from autoui.capture.CaptureMethodBase import CaptureMethodBase
from autoui.capture.utils import BGRA_CHANNEL_COUNT, WGC_MIN_BUILD, WINDOWS_BUILD_NUMBER, get_direct3d_device, is_valid_hwnd

WGC_NO_BORDER_MIN_BUILD = 20348
LEARNING_MODE_DEVICE_BUILD = 17763
"""https://learn.microsoft.com/en-us/uwp/api/windows.ai.machinelearning.learningmodeldevice"""


class WindowsGraphicsCaptureMethod(CaptureMethodBase):
    name = "Windows Graphics Capture"
    short_description = "fast, most compatible, capped at 60fps"
    description = (
        f"\nOnly available in Windows 10.0.{WGC_MIN_BUILD} and up. "
        + f"\nDue to current technical limitations, Windows versions below 10.0.0.{LEARNING_MODE_DEVICE_BUILD}"
        + "\nrequire having at least one audio or video Capture Device connected and enabled."
        + "\nAllows recording UWP apps, Hardware Accelerated and Exclusive Fullscreen windows. "
        + "\nAdds a yellow border on Windows 10 (not on Windows 11)."
        + "\nCaps at around 60 FPS. "
    )
    visible = True
    x = 0
    y = 0
    width = 0
    height = 0
    title_height = 0
    border = 0
    size: SizeInt32
    frame_pool: Direct3D11CaptureFramePool | None = None
    session: GraphicsCaptureSession | None = None
    """This is stored to prevent session from being garbage collected"""

    hwnd = None

    def __init__(self, title = ""):
        super().__init__()
        self.title = title
        self.hwnd = win32gui.FindWindow(None, title)
        if not self.hwnd:
            print("window {title} not found")
            return

        item = create_for_window(self.hwnd)
        self.size = item.size
        
        frame_pool = Direct3D11CaptureFramePool.create_free_threaded(
            get_direct3d_device(),
            DirectXPixelFormat.B8_G8_R8_A8_UINT_NORMALIZED,
            1,
            item.size,
        )
        if not frame_pool:
            raise OSError("Unable to create a frame pool for a capture session.")
        session = frame_pool.create_capture_session(item)
        if not session:
            raise OSError("Unable to create a capture session.")
        session.is_cursor_capture_enabled = False
        if WINDOWS_BUILD_NUMBER >= WGC_NO_BORDER_MIN_BUILD:
            session.is_border_required = False        
        self.session = session
        self.frame_pool = frame_pool  
        session.start_capture()

        self.thread = threading.Thread(target=self.update_window_size)        
        self.exit_event = threading.Event()   
        self.do_update_window_size()
        self.thread.start()

    @override
    def close(self):
        if self.frame_pool:
            self.frame_pool.close()
            self.frame_pool = None
        if self.session:
            try:
                self.session.close()
            except OSError:
                # OSError: The application called an interface that was marshalled for a different thread
                # This still seems to close the session and prevent the following hard crash in LiveSplit
                # "AutoSplit.exe	<process started at 00:05:37.020 has terminated with 0xc0000409 (EXCEPTION_STACK_BUFFER_OVERRUN)>" # noqa: E501
                pass
            self.session = None
    
    def add_window_change_listener(self, listener):
        self.window_change_listeners.append(listener)
        listener.window_changed(self.visible, self.x, self.y, self.border,self.title_height,self.width, self.height,self.scaling)

    def update_window_size(self):
        while not self.exit_event.is_set():            
            self.do_update_window_size()
            self.exit_event.wait(0.01)

    def get_abs_cords(self, x, y):
        return int(self.x + (self.border + x)/self.scaling), int(self.y + (y + self.title_height)/self.scaling)
    
    def do_update_window_size(self):
        x, y, border, title_height, window_width, window_height, scaling = get_window_bounds(self.hwnd, self.top_cut, self.bottom_cut,self.left_cut,self.right_cut)
        visible = is_foreground_window(self.hwnd)
        if  self.title_height != title_height or self.border != border or visible != self.visible or self.x != x or self.y != y or self.width != window_width or self.height != window_height:
            print(f"update_window_size: {x} {y} {title_height} {border} {window_width} {window_height}")
            self.visible = visible
            self.x = x #border_width
            self.y = y #titlebar_with_border_height
            self.title_height = title_height
            self.border = border
            self.width = window_width #client_width
            self.height = window_height #client_height - border_width * 2
            self.scaling = scaling
            for listener in self.window_change_listeners:
                listener.window_changed(visible, x, y,border, title_height, window_width, window_height,scaling)
        
    @override
    def get_frame(self) -> MatLike | None:
        # We still need to check the hwnd because WGC will return a blank black image
        if not (
            self.check_selected_region_exists()
            # Only needed for the type-checker
            and self.frame_pool
        ):
            return None

        try:
            frame = self.frame_pool.try_get_next_frame()
        # Frame pool is closed
        except OSError:
            return None  

        if not frame:
            # print("try_get_next_frame none")
            return None
            
        async def coroutine():
            return await SoftwareBitmap.create_copy_from_surface_async(frame.surface)

        try:
            software_bitmap = asyncio.run(coroutine())
            frame.close()
        except SystemError as exception:
            # HACK: can happen when closing the GraphicsCapturePicker
            if str(exception).endswith("returned a result with an error set"):
                print("return last_captured frame result with an error set")
                return None
            raise

        if not software_bitmap:
            print("return last_captured frame")
            # HACK: Can happen when starting the region selector
            return None
            # raise ValueError("Unable to convert Direct3D11CaptureFrame to SoftwareBitmap.")
        bitmap_buffer = software_bitmap.lock_buffer(BitmapBufferAccessMode.READ_WRITE)
        if not bitmap_buffer:
            raise ValueError("Unable to obtain the BitmapBuffer from SoftwareBitmap.")
        reference = bitmap_buffer.create_reference()
        image = np.frombuffer(cast(bytes, reference), dtype=np.uint8)
        # print(f"image.shape {self.title_height,self.border, self.size.height, self.size.width}")
        image.shape = (self.size.height, self.size.width, BGRA_CHANNEL_COUNT)
        image = image[
            self.title_height: self.title_height + self.height,
            self.border: self.border + self.width
        ]        
        return image

    @override
    def recover_window(self, captured_window_title: str, autosplit: "AutoSplit"):
        hwnd = win32gui.FindWindow(None, captured_window_title)
        if not is_valid_hwnd(hwnd):
            return False
        autosplit.hwnd = hwnd
        try:
            self.reinitialize(autosplit)
        # Unrecordable hwnd found as the game is crashing
        except OSError as exception:
            if str(exception).endswith("The parameter is incorrect"):
                return False
            raise
        return self.check_selected_region_exists(autosplit)

    @override
    def check_selected_region_exists(self, ):
        return bool(
            is_valid_hwnd(self.hwnd)
            and self.frame_pool
            and self.session,
        )  
      
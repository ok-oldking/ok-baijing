# original https://github.com/dantmnf & https://github.com/hakaboom/winAuto
import ctypes
import ctypes.wintypes
import threading

import numpy as np
from typing_extensions import override
from win32 import win32gui

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod
from autoui.capture.utils import is_valid_hwnd, WINDOWS_BUILD_NUMBER
from autoui.capture.window import is_foreground_window, get_window_bounds
from autoui.rotypes.Windows.Graphics.Capture import Direct3D11CaptureFramePool, IGraphicsCaptureItemInterop, \
    IGraphicsCaptureItem, GraphicsCaptureItem
from autoui.rotypes.Windows.Graphics.DirectX import DirectXPixelFormat
from autoui.rotypes.Windows.Graphics.DirectX.Direct3D11 import IDirect3DDevice, CreateDirect3D11DeviceFromDXGIDevice, \
    IDirect3DDxgiInterfaceAccess
from autoui.rotypes.roapi import GetActivationFactory
from . import d3d11
from ..rotypes import IInspectable
from ..rotypes.Windows.Foundation import TypedEventHandler

PBYTE = ctypes.POINTER(ctypes.c_ubyte)
WGC_NO_BORDER_MIN_BUILD = 20348


class WindowsCaptureMethodGraphics(BaseCaptureMethod):
    name = "Windows Graphics Capture"
    short_description = "fast, most compatible, capped at 60fps"
    visible = True
    x = 0
    y = 0
    width = 0
    height = 0
    title_height = 0
    border = 0
    """This is stored to prevent session from being garbage collected"""

    hwnd = None

    def __init__(self, title="", exit_event=threading.Event()):
        super().__init__()
        self.title = title
        self.visible = False
        self.hwnd = win32gui.FindWindow(None, title)
        if not self.hwnd:
            raise Exception(f"window {title} not found")
        self._rtdevice = IDirect3DDevice()
        self._dxdevice = d3d11.ID3D11Device()
        self._immediatedc = d3d11.ID3D11DeviceContext()

        self.start(self.hwnd)

        self.thread = threading.Thread(target=self.update_window_size)
        self.exit_event = exit_event
        self.do_update_window_size()
        self.thread.start()

    def _frame_arrived_callback(self, x, y):
        # print("Frame arrived")
        pass

    def start(self, hwnd, capture_cursor=False):
        self._create_device()
        interop = GetActivationFactory('Windows.Graphics.Capture.GraphicsCaptureItem').astype(
            IGraphicsCaptureItemInterop)
        item = interop.CreateForWindow(hwnd, IGraphicsCaptureItem.GUID)
        self._item = item
        self._last_size = item.Size
        delegate = TypedEventHandler(GraphicsCaptureItem, IInspectable).delegate(
            self.close)
        self._evtoken = item.add_Closed(delegate)
        self.frame_pool = Direct3D11CaptureFramePool.CreateFreeThreaded(self._rtdevice,
                                                                        DirectXPixelFormat.B8G8R8A8UIntNormalized,
                                                                        1, item.Size)
        self.session = self.frame_pool.CreateCaptureSession(item)
        pool = self.frame_pool
        pool.add_FrameArrived(
            TypedEventHandler(Direct3D11CaptureFramePool, IInspectable).delegate(
                self._frame_arrived_callback))
        self.session.IsCursorCaptureEnabled = capture_cursor
        if WINDOWS_BUILD_NUMBER >= WGC_NO_BORDER_MIN_BUILD:
            print(f"Build number {WINDOWS_BUILD_NUMBER} is_border_required = False")
            self.session.IsBorderRequired = False
        self.session.StartCapture()

    def _create_device(self):
        d3d11.D3D11CreateDevice(
            None,
            d3d11.D3D_DRIVER_TYPE_HARDWARE,
            None,
            d3d11.D3D11_CREATE_DEVICE_BGRA_SUPPORT,
            None,
            0,
            d3d11.D3D11_SDK_VERSION,
            ctypes.byref(self._dxdevice),
            None,
            ctypes.byref(self._immediatedc)
        )
        self._rtdevice = CreateDirect3D11DeviceFromDXGIDevice(self._dxdevice)
        self._evtoken = None

    @override
    def close(self):
        self.exit_event.set()
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
        listener.window_changed(self.visible, self.x, self.y, self.border, self.title_height, self.width, self.height,
                                self.scaling)

    def update_window_size(self):
        while not self.exit_event.is_set():
            self.do_update_window_size()
            self.exit_event.wait(0.01)

    def bring_to_front(self):
        if not self.visible:
            win32gui.SetForegroundWindow(self.hwnd)
            self.do_update_window_size()
        return self.visible

    def get_abs_cords(self, x, y):
        return int(self.x + (self.border + x) / self.scaling), int(self.y + (y + self.title_height) / self.scaling)

    def do_update_window_size(self):
        x, y, border, title_height, window_width, window_height, scaling = get_window_bounds(self.hwnd, self.top_cut,
                                                                                             self.bottom_cut,
                                                                                             self.left_cut,
                                                                                             self.right_cut)
        visible = is_foreground_window(self.hwnd)
        if self.title_height != title_height or self.border != border or visible != self.visible or self.x != x or self.y != y or self.width != window_width or self.height != window_height:
            print(f"update_window_size: {x} {y} {title_height} {border} {window_width} {window_height}")
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

    def get_frame(self):
        frame = self.frame_pool.TryGetNextFrame()
        if not frame:
            return None
        img = None
        with frame:
            need_reset_framepool = False
            need_reset_device = False
            if frame.ContentSize.Width != self._last_size.Width or frame.ContentSize.Height != self._last_size.Height:
                # print('size changed')
                need_reset_framepool = True
                self._last_size = frame.ContentSize

            if need_reset_framepool:
                self._reset_framepool(frame.ContentSize)
                return self.get_frame()
            tex = None
            cputex = None
            try:
                tex = frame.Surface.astype(IDirect3DDxgiInterfaceAccess).GetInterface(
                    d3d11.ID3D11Texture2D.GUID).astype(d3d11.ID3D11Texture2D)
                desc = tex.GetDesc()
                desc2 = d3d11.D3D11_TEXTURE2D_DESC()
                desc2.Width = desc.Width
                desc2.Height = desc.Height
                desc2.MipLevels = desc.MipLevels
                desc2.ArraySize = desc.ArraySize
                desc2.Format = desc.Format
                desc2.SampleDesc = desc.SampleDesc
                desc2.Usage = d3d11.D3D11_USAGE_STAGING
                desc2.CPUAccessFlags = d3d11.D3D11_CPU_ACCESS_READ
                desc2.BindFlags = 0
                desc2.MiscFlags = 0
                cputex = self._dxdevice.CreateTexture2D(ctypes.byref(desc2), None)
                self._immediatedc.CopyResource(cputex, tex)
                mapinfo = self._immediatedc.Map(cputex, 0, d3d11.D3D11_MAP_READ, 0)
                img = np.ctypeslib.as_array(ctypes.cast(mapinfo.pData, PBYTE),
                                            (desc.Height, mapinfo.RowPitch // 4, 4))[
                      :, :desc.Width].copy()
                self._immediatedc.Unmap(cputex, 0)
            except OSError as e:
                if e.winerror == d3d11.DXGI_ERROR_DEVICE_REMOVED or e.winerror == d3d11.DXGI_ERROR_DEVICE_RESET:
                    need_reset_framepool = True
                    need_reset_device = True
                else:
                    raise
            finally:
                if tex is not None:
                    tex.Release()
                if cputex is not None:
                    cputex.Release()
            if need_reset_framepool:
                self._reset_framepool(frame.ContentSize, need_reset_device)
                return self.get_frame()
        return img

    def _reset_framepool(self, size, reset_device=False):
        if reset_device:
            self._create_device()
        self.frame_pool.Recreate(self._rtdevice,
                                 DirectXPixelFormat.B8G8R8A8UIntNormalized, 1, size)

    # @override
    # def get_frame(self) -> MatLike | None:
    #     # We still need to check the hwnd because WGC will return a blank black image
    #     if not (
    #             self.check_selected_region_exists()
    #             # Only needed for the type-checker
    #             and self.frame_pool
    #     ):
    #         return None
    #
    #     try:
    #         frame = self.frame_pool.TryGetNextFrame()
    #     # Frame pool is closed
    #     except OSError:
    #         print("try_get_next_frame OSError")
    #         return None
    #
    #     if not frame:
    #         print("try_get_next_frame none")
    #         return None
    #
    #     async def coroutine():
    #         return await SoftwareBitmap.CreateCopyWithAlphaFromBuffer(frame.Surface)
    #
    #     try:
    #         software_bitmap = asyncio.run(coroutine())
    #         frame.close()
    #     except SystemError as exception:
    #         # HACK: can happen when closing the GraphicsCapturePicker
    #         if str(exception).endswith("returned a result with an error set"):
    #             print("return last_captured frame result with an error set")
    #             return None
    #         raise
    #
    #     if not software_bitmap:
    #         print("return last_captured frame")
    #         # HACK: Can happen when starting the region selector
    #         return None
    #         # raise ValueError("Unable to convert Direct3D11CaptureFrame to SoftwareBitmap.")
    #     bitmap_buffer = software_bitmap.lock_buffer(BitmapBufferAccessMode.READ_WRITE)
    #     if not bitmap_buffer:
    #         raise ValueError("Unable to obtain the BitmapBuffer from SoftwareBitmap.")
    #     reference = bitmap_buffer.create_reference()
    #     image = np.frombuffer(cast(bytes, reference), dtype=np.uint8)
    #     # print(f"image.shape {self.title_height,self.border, self.size.height, self.size.width}")
    #     image.shape = (self.size.height, self.size.width, BGRA_CHANNEL_COUNT)
    #     image = image[
    #             self.title_height: self.title_height + self.height,
    #             self.border: self.border + self.width
    #             ]
    #     return image

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

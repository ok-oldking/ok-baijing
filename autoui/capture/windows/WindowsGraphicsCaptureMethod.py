# original https://github.com/dantmnf & https://github.com/hakaboom/winAuto
import ctypes
import ctypes.wintypes
import time

import numpy as np
from typing_extensions import override

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod
from autoui.capture.HwndWindow import HwndWindow
from autoui.capture.windows import d3d11
from autoui.capture.windows.utils import WINDOWS_BUILD_NUMBER
from autoui.logging.Logger import get_logger
from autoui.rotypes import IInspectable
from autoui.rotypes.Windows.Foundation import TypedEventHandler
from autoui.rotypes.Windows.Graphics.Capture import Direct3D11CaptureFramePool, IGraphicsCaptureItemInterop, \
    IGraphicsCaptureItem, GraphicsCaptureItem
from autoui.rotypes.Windows.Graphics.DirectX import DirectXPixelFormat
from autoui.rotypes.Windows.Graphics.DirectX.Direct3D11 import IDirect3DDevice, CreateDirect3D11DeviceFromDXGIDevice, \
    IDirect3DDxgiInterfaceAccess
from autoui.rotypes.roapi import GetActivationFactory

PBYTE = ctypes.POINTER(ctypes.c_ubyte)
WGC_NO_BORDER_MIN_BUILD = 20348

logger = get_logger(__name__)


class WindowsGraphicsCaptureMethod(BaseCaptureMethod):
    name = "Windows Graphics Capture"
    description = "fast, most compatible, capped at 60fps"
    last_frame = None
    last_frame_time = 0
    hwnd_window: HwndWindow = None

    def __init__(self, hwnd_window: HwndWindow):
        super().__init__()
        self.hwnd_window = hwnd_window

        self._rtdevice = IDirect3DDevice()
        self._dxdevice = d3d11.ID3D11Device()
        self._immediatedc = d3d11.ID3D11DeviceContext()

        self.start()

    def _frame_arrived_callback(self, x, y):
        # print("Frame arrived")
        frame = self.frame_pool.TryGetNextFrame()
        if not frame:
            return
        self.last_frame_time = time.time()
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
                return
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
        self.last_frame = img

    def start(self, capture_cursor=False):
        self._create_device()
        interop = GetActivationFactory('Windows.Graphics.Capture.GraphicsCaptureItem').astype(
            IGraphicsCaptureItemInterop)
        item = interop.CreateForWindow(self.hwnd_window.hwnd, IGraphicsCaptureItem.GUID)
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

    def get_frame(self):
        # print(f"WindowsGraphicsCaptureMethod:get_frame {self.hwnd_window.title_height} {self.hwnd_window.border}")
        frame = self.last_frame
        self.last_frame = None
        latency = time.time() - self.last_frame_time
        self.last_frame_time = time.time()
        if latency > 1:
            logger.warning(f"latency too large return None frame: {latency}")
            return None
        if frame is not None and self.hwnd_window.title_height != 0 and self.hwnd_window.border != 0:
            frame = crop_image(frame, self.hwnd_window.border, self.hwnd_window.title_height)

        if frame is not None:
            new_height, new_width = frame.shape[:2]
            self.width = new_width
            self.height = new_height
            self.hwnd_window.update_frame_size(new_width, new_height)

            if frame.shape[2] == 4:
                frame = frame[:, :, :3]

        return frame

    def _reset_framepool(self, size, reset_device=False):
        if reset_device:
            self._create_device()
        self.frame_pool.Recreate(self._rtdevice,
                                 DirectXPixelFormat.B8G8R8A8UIntNormalized, 1, size)

    def get_abs_cords(self, x, y):
        return self.hwnd_window.get_abs_cords(x, y)

    def clickable(self):
        return self.hwnd_window.visible


def crop_image(image, border, title_height):
    # Load the image
    # Image dimensions
    height, width = image.shape[:2]

    # Calculate the coordinates for the bottom-right corner
    x2 = width - border
    y2 = height - border

    # Crop the image
    cropped_image = image[title_height:y2, border:x2]

    # print(f"cropped image: {title_height}-{y2}, {border}-{x2} {cropped_image.shape}")
    #
    # cv2.imshow('Image Window', cropped_image)
    #
    # # Wait for any key to be pressed before closing the window
    # cv2.waitKey(0)

    return cropped_image

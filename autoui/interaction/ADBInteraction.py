from autoui.capture.BaseCaptureMethod import BaseCaptureMethod
from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import BaseOverlay


class ADBInteraction:

    def __init__(self, device, capture: BaseCaptureMethod, overlay: BaseOverlay = None):
        self.overlay = overlay
        self.capture = capture
        self.device = device

    def send_key(self, key, down_time=0.02):
        pass

    def left_click_relative(self, x, y):
        self.left_click(int(self.capture.width * x), int(self.capture.height * y))

    def left_click_box(self, box: Box):
        x, y = box.center_with_variance()
        self.left_click(x, y)

    def left_click(self, x=-1, y=-1):
        self.device.shell(f"tap x y")

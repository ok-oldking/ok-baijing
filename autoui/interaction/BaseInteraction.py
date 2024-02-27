from autoui.feature.Box import Box
from autoui.overlay.BaseOverlay import draw_boxes


class BaseInteraction:

    def __init__(self, capture, overlay):
        self.capture = capture
        self.overlay = overlay

    def send_key(self, key, down_time=0.02):
        pass

    def click_relative(self, x, y):
        self.click(int(self.capture.width * x), int(self.capture.height * y))

    def click_box(self, box: Box, relative_x=0.5, relative_y=0.5):
        print(f"BaseInteraction: click_box {box}")
        draw_boxes(self, "click", [box])
        x, y = box.relative_with_variance(relative_x, relative_y)
        self.click(x, y)

    def click(self, x=-1, y=-1):
        print(f"BaseInteraction: click {x, y}")
        pass

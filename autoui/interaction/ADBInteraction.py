from autoui.interaction.BaseInteraction import BaseInteraction


class ADBBaseInteraction(BaseInteraction):

    def __init__(self, device, capture, width, height, overlay=None):
        super().__init__(capture, overlay)
        self.device = device
        self.width = width
        self.height = height

    def send_key(self, key, down_time=0.02):
        super().send_key(key, down_time)
        self.device.shell(f"input keyevent {key}")

    def click(self, x=-1, y=-1):
        super().click(x, y)
        x = int(x * self.width / self.capture.width)
        y = int(y * self.height / self.capture.height)
        self.device.shell(f"input tap {x} {y}")

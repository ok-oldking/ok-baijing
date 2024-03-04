from autoui.interaction.BaseInteraction import BaseInteraction


class ADBBaseInteraction(BaseInteraction):

    def __init__(self, device, capture, overlay):
        super().__init__(capture, overlay)
        self.device = device

    def send_key(self, key, down_time=0.02):
        super().send_key(key, down_time)
        self.device.shell(f"input keyevent {key}")

    def click(self, x=-1, y=-1):
        super().click(x, y)
        self.device.shell(f"input tap {x} {y}")
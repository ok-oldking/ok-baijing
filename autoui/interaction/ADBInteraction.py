from autoui.interaction.BaseInteraction import BaseInteraction


class ADBBaseInteraction(BaseInteraction):

    def __init__(self, device, capture, overlay):
        super().__init__(capture)
        self.device = device
        self.overlay = overlay

    def send_key(self, key, down_time=0.02):
        pass

    def click(self, x=-1, y=-1):
        print(f"ADBBaseInteraction tap {x} {y}")
        self.device.shell(f"input tap {x} {y}")

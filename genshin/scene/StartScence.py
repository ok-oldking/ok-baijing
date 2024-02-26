from autoui.scene.FeatureScene import FindFeatureScene


class StartScene(FindFeatureScene):
    button_start_power_down = None
    button_start_exit = None
    button_start_note = None

    def detect(self, frame):
        self.button_start_note = self.find_one(frame, "button_start_note", 0.05, 0.10)
        if self.button_start_note is None:
            return False
        self.button_start_exit = self.find_one(frame, "button_start_exit", 0.05, 0.10)
        if self.button_start_exit is None:
            return False
        self.button_start_power_down = self.find_one(frame, "button_start_power_down", 0.05, 0.10)
        if self.button_start_power_down is None:
            return False
        # self.button_start_wrench = self.find_one(frame, "button_start_wrench", 0.05, 0.10)
        return True

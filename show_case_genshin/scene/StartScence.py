from ok.scene.FeatureScene import FindFeatureScene


class StartScene(FindFeatureScene):
    button_start_power_down = None
    button_start_exit = None
    button_start_note = None

    def detect(self, frame):
        return self.find_and_set(["button_start_note", "button_start_exit", "button_start_power_down"], 0.1, 0.1)

from autohelper.scene.FeatureScene import FindFeatureScene


class MonthlyCardScene(FindFeatureScene):
    button_start_power_down = None
    button_start_exit = None
    button_start_note = None

    def detect(self, frame):
        return (self.find_one("image_month_card", 0.05, 0.10) is not None) or (
                self.find_one("image_gem_pop_up", 0.05, 0.10) is not None)

from autoui.scene.FeatureScene import FeatureScene


class StartScene(FeatureScene):

    def detect(self, frame):
        return self.find_one(frame, "menu_start_screen") is not None

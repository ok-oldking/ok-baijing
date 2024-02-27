from autoui.scene.FeatureScene import FindFeatureScene


class StartScene(FindFeatureScene):

    def detect(self, frame):
        return self.find_one("menu_start_screen") is not None

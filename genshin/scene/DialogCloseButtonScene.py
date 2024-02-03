from autoui.scene.FeatureScene import FeatureScene


class DialogCloseButtonScene(FeatureScene):
    close_button = None

    def detect(self, frame):
        self.close_button = self.find_one(frame, "dialog_close_button")
        return self.close_button is not None

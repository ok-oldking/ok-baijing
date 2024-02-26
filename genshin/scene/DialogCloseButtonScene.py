from autoui.scene.FeatureScene import FindFeatureScene


class DialogCloseButtonScene(FindFeatureScene):
    close_button = None

    def detect(self, frame):
        self.close_button = self.find_one(frame, "dialog_close_button")
        return self.close_button is not None

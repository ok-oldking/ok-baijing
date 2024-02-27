from autoui.scene.FeatureScene import FindFeatureScene


class OkDialogScene(FindFeatureScene):
    dialog_ok = None

    def detect(self, frame):
        self.dialog_ok = self.find_one("dialog_ok", 0.5, 0.5)
        return self.dialog_ok is not None

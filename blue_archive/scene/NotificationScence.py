from autoui.scene.FeatureScene import FindFeatureScene


class NotificationScene(FindFeatureScene):
    close_event = None

    def detect(self, frame):
        self.close_event = self.find_one("close_event", 0.2, 0.2)
        return self.close_event is not None

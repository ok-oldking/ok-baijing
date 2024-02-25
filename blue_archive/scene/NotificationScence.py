from autoui.scene.FeatureScene import FeatureScene


class NotificationScene(FeatureScene):
    close_event = None

    def detect(self, frame):
        self.close_event = self.find_one(frame, "close_event")
        return self.close_event is not None

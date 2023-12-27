from autoui.feature.Box import Box
from autoui.scene.FeatureScene import FeatureScene


class DialogScene(FeatureScene):
    button_pause: Box = None
    button_pause_transparent: Box = None
    button_play: Box = None

    def detect(self, frame):
        self.button_pause = self.find_one(frame, "button_pause", 0.05, 0.05)
        self.button_pause_transparent = self.find_one(frame, "button_pause_transparent", 0.05, 0.05)
        self.button_play = self.find_one(frame, "button_play", 0.05, 0.05)
        return self.button_pause or self.button_pause_transparent or self.button_play

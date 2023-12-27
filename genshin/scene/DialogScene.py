from autoui.feature.Box import Box
from autoui.feature.FeatureSet import FeatureSet
from autoui.scene.Scene import Scene


class DialogScene(Scene):
    button_pause: Box = None
    button_pause_transparent: Box = None
    button_play: Box = None

    def __init__(self, feature_set: FeatureSet):
        super().__init__()
        self.feature_set = feature_set

    def detect(self, frame):
        self.button_pause = self.feature_set.find_one(frame, "button_pause", 0.05, 0.05)
        self.button_pause_transparent = self.feature_set.find_one(frame, "button_pause_transparent", 0.05, 0.05)
        self.button_play = self.feature_set.find_one(frame, "button_play", 0.05, 0.05)
        return self.button_pause or self.button_pause_transparent or self.button_play

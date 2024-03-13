from autohelper.feature.Box import Box
from autohelper.scene.FeatureScene import FindFeatureScene


class DialogPlayingScene(FindFeatureScene):
    button_pause: Box = None
    button_pause_transparent: Box = None
    button_play: Box = None

    def detect(self, frame):
        self.button_pause = self.find_one("button_pause", 0.05, 0.05)
        self.button_play = self.find_one("button_play", 0.05, 0.05)
        return (self.button_pause or self.button_play) and len(self.find("button_dialog", 0.5, 0.5)) == 0

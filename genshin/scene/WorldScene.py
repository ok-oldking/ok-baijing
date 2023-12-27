from autoui.feature.FeatureSet import FeatureSet
from autoui.scene.Scene import Scene


class WorldScene(Scene):

    def __init__(self, feature_set: FeatureSet):
        super().__init__()
        self.feature_set = feature_set

    def detect(self, frame):
        features_found = 0
        if self.feature_set.find_one(frame, "label_char_1", 0.05, 0.10):
            features_found += 1
        if self.feature_set.find_one(frame, "label_char_2", 0.05, 0.10):
            features_found += 1
        if self.feature_set.find_one(frame, "label_char_3", 0.05, 0.10):
            features_found += 1
        if self.feature_set.find_one(frame, "label_char_4", 0.05, 0.10):
            features_found += 1
        return features_found >= 3

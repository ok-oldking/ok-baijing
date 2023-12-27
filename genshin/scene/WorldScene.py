from autoui.scene.FeatureScene import FeatureScene


class WorldScene(FeatureScene):

    def detect(self, frame):
        features_found = 0
        if self.find_one(frame, "label_char_1", 0.05, 0.10):
            features_found += 1
        if self.find_one(frame, "label_char_2", 0.05, 0.10):
            features_found += 1
        if self.find_one(frame, "label_char_3", 0.05, 0.10):
            features_found += 1
        if self.find_one(frame, "label_char_4", 0.05, 0.10):
            features_found += 1
        return features_found >= 3

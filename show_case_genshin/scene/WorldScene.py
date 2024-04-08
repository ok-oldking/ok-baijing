from ok.scene.FeatureScene import FindFeatureScene


class WorldScene(FindFeatureScene):

    def detect(self, frame):
        return self.find_one("top_left_paimon", 0.05, 0.05) is not None

from autoui.scene.FeatureScene import FeatureScene


class WorldScene(FeatureScene):

    def detect(self, frame):
        if self.find_one(frame, "top_left_paimon", 0.05, 0.05):
            return True

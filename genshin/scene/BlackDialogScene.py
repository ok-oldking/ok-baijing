from autoui.color.Color import calculate_color_percentage, black_color
from autoui.scene.FeatureScene import FeatureScene


class BlackDialogScene(FeatureScene):

    def detect(self, frame):
        return calculate_color_percentage(frame, black_color) > 0.9

from autohelper.color.Color import calculate_color_percentage, black_color
from autohelper.scene.FeatureScene import FindFeatureScene


class BlackDialogScene(FindFeatureScene):

    def detect(self, frame):
        return calculate_color_percentage(frame, black_color) > 0.9

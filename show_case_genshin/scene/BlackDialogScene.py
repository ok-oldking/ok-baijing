from autohelper.color.Color import calculate_color_percentage, black_color
from autohelper.scene.FeatureScene import FindFeatureScene


class BlackDialogScene(FindFeatureScene):

    def detect(self, frame):
        if calculate_color_percentage(frame, black_color) > 0.9:
            self.sleep(3)
            frame = self.next_frame()
            if calculate_color_percentage(frame, black_color) > 0.9:
                return True

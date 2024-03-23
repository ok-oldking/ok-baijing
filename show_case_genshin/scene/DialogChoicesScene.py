from typing import List

from autohelper.feature.Box import Box
from autohelper.scene.FeatureScene import FindFeatureScene
from show_case_genshin.matching.choice import find_choices


class DialogChoicesScene(FindFeatureScene):
    button_pause: Box = None
    button_pause_transparent: Box = None
    button_play: Box = None
    dialogs: List[Box] = []
    dialog_vertical_distance = 0

    def detect(self, frame):
        self.dialogs = self.find("button_dialog", 0.3, 0.3, 0.9)
        if len(self.dialogs) > 0:  # try to find dialog choices and click the first
            if len(self.dialogs) > 1:
                self.dialog_vertical_distance = abs(self.dialogs[0].y - self.dialogs[1].y)
                # print(f"AutoDialogTask: dialog_vertical_distance {self.dialog_vertical_distance}")
            if self.dialog_vertical_distance == 0:
                self.dialog_vertical_distance = round(self.dialogs[0].height * 2.08333333333)
            choices = find_choices(frame, self.dialogs[0], vertical=-self.dialog_vertical_distance, threshold=0.3)
            self.draw_boxes("choices", choices)
            above_count = len(choices)
            if above_count > 0:
                self.logger.info(
                    f"AutoDialogTask: Found {above_count} choices above dialog, won't click {self.dialog_vertical_distance} {self.dialogs[0].height}")
                return False
            return True
        return False

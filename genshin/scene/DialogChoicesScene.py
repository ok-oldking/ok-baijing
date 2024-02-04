from typing import List

from autoui.feature.Box import Box
from autoui.scene.FeatureScene import FeatureScene
from genshin.matching.choice import find_choices


class DialogChoicesScene(FeatureScene):
    button_pause: Box = None
    button_pause_transparent: Box = None
    button_play: Box = None
    dialogs: List[Box] = []
    dialog_vertical_distance = 0

    def detect(self, frame):
        self.dialogs = self.find(frame, "button_dialog", 0.3, 0.3, 0.9)
        if len(self.dialogs) > 0:  # try to find dialog choices and click the first
            if len(self.dialogs) > 1:
                self.dialog_vertical_distance = abs(self.dialogs[0].y - self.dialogs[1].y)
                # print(f"AutoDialogTask: dialog_vertical_distance {self.dialog_vertical_distance}")
            if self.dialog_vertical_distance == 0:
                self.dialog_vertical_distance = self.dialogs[0].height
            choices = find_choices(frame, self.dialogs[0], vertical=-self.dialog_vertical_distance, threshold=0.6)
            self.draw_boxes("choices", choices)
            above_count = len(choices)
            if above_count > 0:
                print(f"AutoDialogTask: Found {above_count} choices above dialog, won't click")
                return False
            return True
        return False

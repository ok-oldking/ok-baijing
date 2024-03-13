import sys
from typing import List

from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate


class FindFeature:

    def __init__(self):
        self.feature_set = None
        self.executor = None

    def find(self, feature_name, horizontal_variance=0, vertical_variance=0, threshold=0) -> List[Box]:
        if self.executor.frame is None:
            return list()
        return self.feature_set.find_feature(self.executor.frame, feature_name, horizontal_variance, vertical_variance,
                                             threshold)

    def wait_and_click(self, feature, horizontal_variance=0, vertical_variance=0, threshold=0, relative_x=0.5,
                       relative_y=0.5,
                       time_out=0, pre_action=None, post_action=None):
        box = self.wait_until(lambda: self.find_one(feature, horizontal_variance, vertical_variance, threshold),
                              time_out,
                              pre_action,
                              post_action)
        if box is not None:
            self.click_box(box, relative_x, relative_y)
            return True
        return False

    def find_one(self, feature_name, horizontal_variance=0, vertical_variance=0, threshold=0) -> Box:
        boxes = self.find(feature_name, horizontal_variance, vertical_variance, threshold)
        if len(boxes) > 0:
            if len(boxes) > 1:
                print(f"find_one:found {feature_name} too many {len(boxes)}", file=sys.stderr)
            return boxes[0]

    @staticmethod
    def draw_boxes(boxes, feature_name):
        communicate.draw_box.emit(feature_name, boxes)

    def on_feature(self, boxes):
        pass

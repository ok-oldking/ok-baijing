import sys
from typing import List

from autoui.feature.Box import Box
from autoui.feature.FeatureSet import FeatureSet


class FindFeature:

    def __init__(self, feature_set: FeatureSet):
        self.feature_set = feature_set

    def find(self, frame, feature_name, horizontal_variance=0, vertical_variance=0, threshold=0) -> List[Box]:
        if frame is None:
            return list()
        return self.feature_set.find_feature(frame, feature_name, horizontal_variance, vertical_variance, threshold)

    def find_one(self, frame, feature_name, horizontal_variance=0, vertical_variance=0, threshold=0) -> Box:
        boxes = self.find(frame, feature_name, horizontal_variance, vertical_variance, threshold)
        if len(boxes) > 1:
            print(f"find_one:found {feature_name} too many {len(boxes)}", file=sys.stderr)
        if len(boxes) == 1:
            return boxes[0]

    def on_feature(self, boxes):
        pass

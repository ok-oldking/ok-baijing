from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.BaseTask import BaseTask
from autoui.overlay.BaseOverlay import BaseOverlay
from autoui.feature.Box import Box
from typing_extensions import override
from typing import List

class FindFeatureTask(BaseTask):
    
    def __init__(self, interaction, feature_set:FeatureSet, horizontal_variance: float = 0, vertical_variance: float = 0):
        super().__init__(interaction) 
        self.feature_set = feature_set
        self.horizontal_variance = horizontal_variance
        self.vertical_variance = vertical_variance
        
    @override
    def run_frame(self, frame):        
        pass

    def find(self, frame, feature_name, horizontal_variance = None, vertical_variance  = None) -> List[Box]:  
        if horizontal_variance is None:
            horizontal_variance = self.horizontal_variance
        if vertical_variance is None:
            vertical_variance = self.vertical_variance       
        boxes = self.feature_set.find_feature(frame, feature_name,horizontal_variance, vertical_variance)
        for box in boxes:
            print(f'Box {feature_name} found at: x={box.x}, y={box.y}, width={box.width}, height={box.height}') 
        if self.interaction.overlay:                
            self.interaction.overlay.draw_boxes(feature_name, boxes, "red")  
        return boxes

    def find_one(self, frame, feature_name, horizontal_variance  = None, vertical_variance  = None)->Box:
        boxes = self.find(frame, feature_name, horizontal_variance, vertical_variance) 
        if len(boxes) > 1:
            print("find_one:found too many len(boxes)", file=sys.stderr)
        if len(boxes) == 1:
            return boxes[0]
        
    def on_feature(self, boxes):
        pass
        

from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.BaseTask import BaseTask

class FindFeatureAndClickTask(BaseTask):

    paused = False
    
    def __init__(self, method : CaptureMethodBase, feature_set:FeatureSet, feature_name: str, wait_time = 0.1,horizontal_variance: float = 0, vertical_variance: float = 0):
        super().__init__(method, wait_time) 
        self.feature_name = feature_name
        self.feature_set = feature_set
        self.horizontal_variance = horizontal_variance
        self.vertical_variance = vertical_variance
        
    def run(self):
        frame = self.method.get_frame()
        if frame is not None:
            boxes = self.feature_set.findFeature(frame, self.feature_name,self.horizontal_variance, self.vertical_variance)
            for box in boxes:
                print(f'Box found at: x={box.x}, y={box.y}, width={box.width}, height={box.height}') 
                self.method.draw_rectangle(box.x,box.y,box.width,box.height)     
        self.exit_event.wait(5)

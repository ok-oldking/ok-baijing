from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.overlay.BaseOverlay import BaseOverlay
from typing_extensions import override
import win32con

class AutoPlayDialogTask(FindFeatureTask):

    def __init__(self,interaction, feature_set: FeatureSet):
        super().__init__(interaction,feature_set, "button_play", 0.1, 0.02)
           
    @override
    def on_feature(self, boxes):  
        print(f"AutoPlayDialogTask click box ${boxes[0]}")    
        self.interaction.left_click_box(boxes)
        # self.interaction.send_key("space")


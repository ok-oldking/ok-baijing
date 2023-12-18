from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.overlay.BaseOverlay import BaseOverlay
from typing_extensions import override
import win32con
import time

class SkipDialogTask(FindFeatureTask):

    def __init__(self, interaction, feature_set: FeatureSet):
        super().__init__(interaction, feature_set,"button_pause", 0.1, 0.02)
    
           
    @override
    def on_feature(self, boxes):        
        self.interaction.send_key("space")
        time.sleep(1)


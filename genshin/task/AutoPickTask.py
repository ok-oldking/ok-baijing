from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from typing_extensions import override
import time

class AutoPickTask(FindFeatureTask):
               
    @override
    def run_frame(self, frame):     
        button_f = self.find_one(frame, "button_f", 0.3,0.3)
        if button_f:
            if not self.find(frame, "button_dialog", 0.7, 0.7): # try find dialog choices and click the first
                print(f"found button_f with no dialog pickup")
                self.interaction.send_key("f")
                time.sleep(0.1)
                self.interaction.send_key("f")
                time.sleep(0.1)
                self.interaction.send_key("f")
                time.sleep(0.1)
         

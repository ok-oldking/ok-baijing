from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from typing_extensions import override
import time

class AutoPickTask(FindFeatureTask):

    last_passed = 0
               
    @override
    def run_frame(self, frame):     
        button_f = self.find_one(frame, "button_f", 0.3,0.3)
        if button_f:
            if self.find(frame, "button_dialog", 0.7, 0.7): # try find dialog choices and click the first
                self.last_passed == 0
            else:
                print(f"found button_f with no dialog pickup") 
                if self.last_passed == 0:
                    self.last_passed = time.time()
                elif time.time() - self.last_passed > 0:          
                    print(f"found twice with no dialog pickup {time.time() - self.last_passed}")
                    self.last_passed = 0              
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)
        else:
            self.last_passed = 0
            
         

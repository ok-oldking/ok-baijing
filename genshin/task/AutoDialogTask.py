from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from typing_extensions import override
import time

class AutoDialogTask(FindFeatureTask):
               
    @override
    def run_frame(self, frame):     
        play_button = self.find_one(frame, "button_play", 0.1, 0.05)
        if play_button:
            if not self.try_find_click_dialog(frame): # try find dialog choices and click the first
                print(f"found button_play click")
                self.interaction.left_click_box(play_button)
                time.sleep(0.4)
            return    
        # find the pause button means we are in a conversation
        pause_button = self.find_one(frame, "button_pause", 0.1, 0.05)
        if pause_button:            
            if not self.try_find_click_dialog(frame):  # no dialog choices, we send space to speed up
                print(f"found pause_button space")
                self.interaction.send_key("space")
                time.sleep(0.4)

    def try_find_click_dialog(self, frame):
        dialogs = self.find(frame, "button_dialog", 0.5, 0.5)
        if len(dialogs) > 0: # try find dialog choices and click the first
            self.interaction.left_click_box(dialogs[0])
            time.sleep(0.4)
            return True

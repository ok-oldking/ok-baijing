from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.feature.FeatureSet import FeatureSet
from autoui.task.FindFeatureTask import FindFeatureTask
from typing_extensions import override
import time

class AutoDialogTask(FindFeatureTask):

    def __init__(self, interaction, feature_set: FeatureSet):
        super().__init__(interaction,feature_set, 0.2, 0.05)
               
    @override
    def run_frame(self, frame):     
        # find the play button, turn on auto play  
        play_button = self.find_one(frame, "button_play")
        if play_button:
            print("found button_play")
            self.interaction.left_click_box(play_button)
            time.sleep(3)
            return
        # find the pause button means we are in a conversation
        pause_button = self.find_one(frame, "button_pause")
        if pause_button:            
            print("found pause_button")
            dialogs = self.find(frame, "button_dialog", 0.5, 0.5)
            if len(dialogs) > 0: # try find dialog choices and click the first
                self.interaction.left_click_box(dialogs[0])
                time.sleep(1)
            else: # no dialog choices, we send space to speed up
                self.interaction.send_key("space")
                time.sleep(1)

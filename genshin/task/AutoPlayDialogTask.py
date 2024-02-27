import time

from typing_extensions import override

from autoui.task.FindFeatureTask import FindFindFeatureTask
from genshin.scene.BlackDialogScene import BlackDialogScene
from genshin.scene.DialogCloseButtonScene import DialogCloseButtonScene
from genshin.scene.DialogPlayingScene import DialogPlayingScene


class AutoPlayDialogTask(FindFindFeatureTask):
    dialog_vertical_distance = 0

    @override
    def run_frame(self):
        # Check if the scene is an instance of DialogPlayingScene or BlackDialogScene
        if self.is_scene((DialogPlayingScene, BlackDialogScene, DialogCloseButtonScene)):
            # For DialogPlayingScene, check if the button_play is present
            if self.is_scene(DialogPlayingScene) and self.scene.button_play:
                print("AutoDialogTask: turn on auto play")
                self.click_box(self.scene.button_play)
            elif self.is_scene(DialogCloseButtonScene):
                print("AutoDialogTask: turn on auto play")
                self.click_box(self.scene.close_button)
            else:
                # This covers the else case for DialogPlayingScene without button_play
                # and all instances of BlackDialogScene
                self.click_relative(0.5, 0.5)
            time.sleep(1)

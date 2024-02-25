import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.BlackDialogScene import BlackDialogScene
from genshin.scene.DialogCloseButtonScene import DialogCloseButtonScene
from genshin.scene.DialogPlayingScene import DialogPlayingScene


class AutoPlayDialogTask(FindFeatureTask):
    dialog_vertical_distance = 0

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        # Check if the scene is an instance of DialogPlayingScene or BlackDialogScene
        if isinstance(scene, (DialogPlayingScene, BlackDialogScene, DialogCloseButtonScene)):
            # For DialogPlayingScene, check if the button_play is present
            if isinstance(scene, DialogPlayingScene) and scene.button_play:
                print("AutoDialogTask: turn on auto play")
                self.interaction.click_box(scene.button_play)
            elif isinstance(scene, DialogCloseButtonScene):
                print("AutoDialogTask: turn on auto play")
                self.interaction.click_box(scene.close_button)
            else:
                # This covers the else case for DialogPlayingScene without button_play
                # and all instances of BlackDialogScene
                self.interaction.click_relative(0.5, 0.5)
            time.sleep(1)

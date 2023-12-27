import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.DialogScene import DialogScene


class AutoDialogTask(FindFeatureTask):

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, DialogScene):
            if scene.button_play:
                # turn on autoplay
                print(f"AutoDialogTask:turn on auto play")
                self.interaction.left_click_box(scene.button_play)
                time.sleep(1)
            elif not self.try_find_click_dialog(frame):  # no dialog choices, we send space to speed up
                print(f"AutoDialogTask:found pause_button space")
                self.interaction.left_click()
                time.sleep(0.5)

    def try_find_click_dialog(self, frame):
        dialogs = self.find(frame, "button_dialog", 0.5, 0.5)
        if len(dialogs) > 0:  # try find dialog choices and click the first
            self.interaction.left_click_box(dialogs[0])
            time.sleep(1)
            return True

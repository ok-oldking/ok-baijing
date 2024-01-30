import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.DialogChoicesScene import DialogChoicesScene


class AutoChooseDialogTask(FindFeatureTask):
    dialog_vertical_distance = 0

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, DialogChoicesScene):
            print(f"AutoChooseDialogTask choose last option")
            self.interaction.left_click_box(scene.dialogs[-1])
            time.sleep(1)

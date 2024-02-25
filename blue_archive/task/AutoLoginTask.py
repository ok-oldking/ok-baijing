import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from blue_archive.scene.StartScence import StartScene


class AutoLoginTask(FindFeatureTask):

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, StartScene):
            print(f"Start scene click")
            self.interaction.click_relative(0.5, 0.5)
            time.sleep(1)

import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.StartScence import StartScene


class AutoLoginTask(FindFeatureTask):

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, StartScene) or isinstance(scene, MonthlyCardScene):
            self.interaction.left_click_relative(0.6, 0.6)
            time.sleep(1)

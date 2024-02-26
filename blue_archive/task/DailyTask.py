import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from blue_archive.scene.MainScene import MainScene


class DailyTask(FindFindFeatureTask):

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, MainScene):
            print(f"DailyTask:click mission")
            executor.click_box(scene.main_screen_mission)
            time.sleep(1)

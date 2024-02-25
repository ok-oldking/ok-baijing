import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from blue_archive.scene.NotificationScence import NotificationScene


class CloseNotificationTask(FindFeatureTask):

    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, NotificationScene):
            print(f"Start scene click")
            executor.click_box(scene.close_event, 0.8)
            time.sleep(1)

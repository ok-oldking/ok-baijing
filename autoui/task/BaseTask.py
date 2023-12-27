from cv2.typing import MatLike

from autoui.scene.Scene import Scene
from autoui.task.TaskExecutor import TaskExecutor


class BaseTask:

    def __init__(self, interaction):
        self.interaction = interaction

    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        pass

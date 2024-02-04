import time

from cv2.typing import MatLike
from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.WorldScene import WorldScene


class AutoPickTask(FindFeatureTask):
    @override
    def run_frame(self, executor: TaskExecutor, scene: Scene, frame: MatLike):
        if isinstance(scene, WorldScene):
            button_f = self.find_one(frame, "button_f", 0.3, 0.3)
            if button_f:
                if not self.has_dialogs(frame):
                    time.sleep(0.1)
                    next_frame = executor.next_frame()
                    if self.find_one(next_frame, "button_f", 0.3, 0.3) and not self.has_dialogs(next_frame):
                        print("AutoPickTask: double check passed click f")
                        self.interaction.send_key("f")
                        time.sleep(0.1)
                        self.interaction.send_key("f")
                        time.sleep(0.1)
                        self.interaction.send_key("f")
                        time.sleep(0.1)
                        self.interaction.send_key("f")
                        time.sleep(0.1)

    def has_dialogs(self, frame: MatLike):
        dialogs = self.find(frame, "button_dialog_world", 0.4, 0.4)
        if len(dialogs) > 0:
            return True
        else:
            return False

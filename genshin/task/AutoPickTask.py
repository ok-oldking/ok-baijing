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
                if self.find(frame, "button_dialog", 0.7, 0.7):  # try find dialog choices and click the first
                    return
                else:
                    time.sleep(0.01)
                    frame = executor.next_frame()
                    if not self.find(frame, "button_dialog", 0.7, 0.7):
                        print(f"found button_f with no dialog pickup")
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)
                    self.interaction.send_key("f")
                    time.sleep(0.1)

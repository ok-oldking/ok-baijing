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
                    time.sleep(0.2)
                    next_frame = executor.next_frame()
                    if self.find_one(next_frame, "button_f", 0.3, 0.3) and not self.has_dialogs(next_frame):
                        print("AutoPickTask: double check passed click f")
                        self.interaction.send_key("f")
                        time.sleep(0.1)
                        self.interaction.send_key("f")
                        time.sleep(0.1)

            # if button_f:  # if there is an f, we want to find only one choice that is not a Dialog
            #     to_find = Box(button_f.x + int(button_f.width * 2.2), button_f.y, button_f.width, button_f.height)
            #     choice = find_choice(frame, to_find, threshold=0.4)
            #     if choice:
            #         self.draw_box("choices", choice)
            #         if True or self.find(frame, "button_dialog", 0.5, 0.5):
            #             return
            #         else:
            #             time.sleep(0.01)
            #             # frame = executor.next_frame()
            #             # if not self.find(frame, "button_dialog", 0.7, 0.7):
            #             #     print(f"found button_f with no dialog pickup")
            #             print(f"found button_f with no dialog pickup")
            #             self.interaction.send_key("f")
            #             time.sleep(0.1)
            #             self.interaction.send_key("f")
            #             time.sleep(0.1)
            #             # self.interaction.send_key("f")
            #             # time.sleep(0.1)
            #             # self.interaction.send_key("f")
            #             # time.sleep(0.1)
            #             # self.interaction.send_key("f")
            #             # time.sleep(0.1)

    def has_dialogs(self, frame: MatLike):
        dialogs = self.find(frame, "button_dialog", 0.4, 0.4)
        if len(dialogs) > 0:
            return True
        else:
            return False

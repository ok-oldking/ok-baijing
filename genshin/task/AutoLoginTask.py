import time

from typing_extensions import override

from autoui.task.FindFeatureTask import FindFindFeatureTask
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.StartScence import StartScene


class AutoLoginTask(FindFindFeatureTask):

    @override
    def run_frame(self):
        # print("run_frame AutoLoginTask")
        if self.is_scene(StartScene) or self.is_scene(MonthlyCardScene):
            print(f"Start scene click")
            self.click_relative(0.6, 0.6)
            time.sleep(1)

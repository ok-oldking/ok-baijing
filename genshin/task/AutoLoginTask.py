from typing_extensions import override

from autohelper.task.FindFeatureTask import FindFeatureTask
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.StartScence import StartScene


class AutoLoginTask(FindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(StartScene) or self.is_scene(MonthlyCardScene):
            self.logger.info(f"AutoLoginTask click")
            self.click_relative(0.6, 0.6)
            self.sleep(1)
            return True

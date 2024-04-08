from typing_extensions import override

from ok.task.FindFeatureTask import FindFeatureTask
from show_case_genshin.scene.MonthlyCardScene import MonthlyCardScene
from show_case_genshin.scene.StartScence import StartScene


class AutoLoginTask(FindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(StartScene) or self.is_scene(MonthlyCardScene):
            self.logger.info(f"AutoLoginTask click")
            self.click_relative(0.5, 0.7)
            self.sleep(1)
            return True

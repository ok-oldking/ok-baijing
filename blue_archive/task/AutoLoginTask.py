from typing_extensions import override

from autoui.task.FindFeatureTask import FindFeatureTask
from blue_archive.scene.StartScence import StartScene


class AutoLoginTask(FindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(StartScene):
            print(f"Start scene click")
            self.click_relative(0.5, 0.5)
            self.sleep(1)

from typing_extensions import override

from autoui.task.FindFeatureTask import FindFeatureTask
from blue_archive.scene.OkDialogScene import OkDialogScene


class ClickOkTask(FindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(OkDialogScene):
            print(f"ClickOkTask: click ok")
            self.click_box(self.scene.dialog_ok)
            self.sleep(1)

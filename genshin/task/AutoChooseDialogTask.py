import time

from typing_extensions import override

from autoui.task.FindFeatureTask import FindFindFeatureTask
from genshin.scene.DialogChoicesScene import DialogChoicesScene


class AutoChooseDialogTask(FindFindFeatureTask):
    dialog_vertical_distance = 0

    @override
    def run_frame(self):
        if self.is_scene(DialogChoicesScene):
            print(f"AutoChooseDialogTask choose first option")
            self.click_box(self.scene.dialogs[0])
            time.sleep(1)

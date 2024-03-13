from typing_extensions import override

from autohelper.task.FindFeatureTask import FindFeatureTask
from genshin.scene.WorldScene import WorldScene


class AutoPickTask(FindFeatureTask):
    @override
    def run_frame(self):
        if self.is_scene(WorldScene):
            button_f = self.find_one("button_f", 0.3, 0.3)
            if button_f:
                if not self.has_dialogs():
                    self.logger.info("found a f")
                    self.sleep(0.1)
                    self.next_frame()
                    if self.find_one("button_f", 0.3, 0.3) and not self.has_dialogs():
                        self.logger.info("double check passed click f")
                        self.send_key("f")
                        self.sleep(0.1)
                        self.send_key("f")
                        self.sleep(0.1)
                        self.send_key("f")
                        self.sleep(0.1)
                        self.send_key("f")
                        self.sleep(0.1)

    def has_dialogs(self):
        dialogs = self.find("button_dialog_world", 0.4, 0.4)
        if len(dialogs) > 0:
            return True
        else:
            return False

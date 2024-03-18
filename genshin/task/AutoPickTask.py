from typing_extensions import override

from autohelper.task.FindFeatureTask import FindFeatureTask
from genshin.matching.choice import find_choices
from genshin.scene.WorldScene import WorldScene


class AutoPickTask(FindFeatureTask):
    button_f = None

    @override
    def run_frame(self):
        if self.is_scene(WorldScene):
            self.button_f = self.find_one("button_f", 0.3, 0.3)
            if self.button_f:
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
                        self.sleep(1)
                        return True

    def has_dialogs(self):
        choices = find_choices(self.frame, self.button_f, horizontal=self.button_f.width * 2.35, limit=1,
                               threshold=0.3)
        if len(choices) > 0:
            return True
        else:
            return False

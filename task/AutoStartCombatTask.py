import re

from ok.ocr.OCR import OCR
from ok.task.TriggerTask import TriggerTask


class AutoStartCombatTask(TriggerTask, OCR):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "自动点开始战斗"
        self.description = "帮助快速过剧情"
        self.default_config = {'_enabled': False}

    def run(self):
        start_combat = self.ocr(0.85, 0.87, 0.96, 0.94, '开始战斗')
        if start_combat:
            self.click_box(start_combat)
            # self.log_info(start_combat)
            self.log_info("点击开始战斗", True)
            self.sleep(2)
            return True
        click_to_continue = self.ocr(0.42, 0.74, 0.58, 0.97, match=re.compile(r"^点击"))
        if click_to_continue:
            self.click_box(click_to_continue)
            return True

from ok.feature.FindFeature import FindFeature
from ok.task.TriggerTask import TriggerTask


class AutoStartCombatTask(TriggerTask, FindFeature):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "自动点开始战斗"
        self.description = "帮助快速过剧情"
        self.default_config = {'_enabled': False}

    def run(self):
        start_combat = self.find_one('start_combat')
        if start_combat:
            self.click_box(start_combat)
            # self.log_info(start_combat)
            self.notification("点击开始战斗")
            self.sleep(2)

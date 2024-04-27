import re

from typing_extensions import override

from ok.feature.Box import find_box_by_name
from task.ManXunTask import ManXunTask, Finished


class AoSkillManXunTask(ManXunTask):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "自动漫巡凹技能"
        self.description = """主界面开始, 凹指定角色指定技能, 达不到要求就自动跳过战斗结束
    """
        self.super_config = self.default_config
        del self.super_config['无法直接胜利, 自动投降跳过']
        self.default_config = {'角色名': '岑缨', '路线': '空想王国', '循环次数': 5,
                               '目标技能': ['职业联动', '针对打击'], '目标技能个数': 2}
        self.default_config = {**self.default_config, **self.super_config}

    @override
    def run(self):
        for i in range(self.config.get('循环次数')):
            self.info.clear()
            self.route = None
            self.info['目前循环次数'] = i + 1
            self.log_info(f'凹技能进行第{self.info["目前循环次数"]} 次')
            if not self.loop_manxun():
                break
        self.log_info("自动漫巡任务结束", notify=True)

    def confirm_generate(self):
        if self.info.get('已获得目标技能个数', 0) < self.config['目标技能个数']:
            return True

    def loop_manxun(self):
        is_main = self.check_is_main()
        if not is_main and not self.check_is_manxun_ui():
            boxes = self.ocr(self.box_of_screen(0.2, 0.5, 0.8, 0.3, "漫巡路线检测区域"), match=self.config['路线'])
            if boxes:
                self.route = boxes[0]
                self.log_debug(f'在漫巡路线选择界面 {self.route}')
            if not self.route:
                self.log_error("必须从主界面或漫巡界面开始", notify=True)
                self.screenshot("必须从主界面或漫巡界面开始")
                return False
        if is_main or self.route:
            self.enter_manxun()
            self.start_manxun()
        while True:
            try:
                self.loop()
            except Finished:
                return True
            except Exception as e:
                self.screenshot(f"运行异常{e}")
                self.log_error(f"运行异常,已暂停:", e, True)
                self.pause()

    def start_manxun(self):
        boxes = self.ocr(self.bottom_button_zone)
        manxun_start = find_box_by_name(boxes, "漫巡开始")
        if not manxun_start:
            self.select_char()
            manxun_start = self.ocr(self.bottom_button_zone, "漫巡开始")
        self.click_box(manxun_start)
        self.wait_until(lambda: self.ocr(self.current_zone, match=re.compile(r"^自动")), time_out=60)
        self.click_relative(0.5, 0.5)

    def if_skip_battle(self):
        if self.info['漫巡深度'] < self.config['深度等级最多提升到']:
            self.log_debug(f"未达到预定深度, 不跳过战斗")
            return False

        self.log_debug(f"检测技能是否满足条件 {self.info.get('已获得目标技能个数', 0)} {self.info.get('获得技能', [])}")
        if self.info.get('已获得目标技能个数', 0) >= self.config['目标技能个数']:
            return False
        else:
            return True

    def check_skills(self):
        current_skills = self.info['获得技能']
        current_count = 0
        skills = {}
        if current_skills:
            for skill in current_skills:
                for target_skill in self.config['目标技能']:
                    if target_skill in skill:
                        current_count += 1
                        skills[skill] = skills.get(skill, 0) + 1
        if current_count != self.info.get('已获得目标技能个数', 0):
            self.info['已获得目标技能个数'] = current_count
            self.info['已获取的目标技能'] = current_skills
            self.notification(f"已经获取到 {current_count}个目标技能 {skills}")

    def select_char(self):
        char_name = self.wait_until(
            lambda: self.ocr(self.box_of_screen(0.4, 0.4, 0.6, 0.5, "角色检测区域"),
                             re.compile(f"{self.config['角色名']}$")),
            time_out=60,
            post_action=lambda: self.swipe_relative(0.8, 0.5, 0.5, 0.5, 1))
        if not char_name:
            raise Exception(f'找不到角色 {self.config["角色名"]}')
        self.click_box(char_name)
        next_step = self.wait_click_box(lambda: self.ocr(self.bottom_button_zone, "下一步"))
        self.wait_click_box(lambda: self.ocr(self.top_right_button_zone, "上次编队"))
        self.sleep(0.5)
        self.click_box(next_step)
        self.wait_click_box(lambda: self.ocr(self.top_right_button_zone, "上次编组"))
        self.sleep(3)
        while True:
            boxes = self.ocr(self.box_of_screen(0.5, 0.5, 0.5, 0.5, "支援记忆烙痕检测区域"),
                             re.compile("选择支援记忆烙痕"))
            if boxes:
                self.notification("没有支援记忆烙痕, 请手动选择后继续!")
                self.screenshot("没有支援记忆烙痕, 请手动选择后继续!")
                self.pause()
            break
        self.sleep(0.5)

    def enter_manxun(self):
        if not self.route:
            self.main_go_to_manxun()
            self.wait_click_box(
                lambda: self.ocr(self.box_of_screen(0.2, 0.5, 0.8, 0.3, "漫巡路线检测区域"), match=self.config['路线']))
        else:
            self.click_box(self.route)
        self.wait_click_box(
            lambda: self.ocr(self.right_button_zone, match='前往回廊漫巡'))
        start_manxun = self.wait_click_box(
            lambda: self.ocr(self.star_combat_zone, match='开始新漫巡'))
        self.sleep(1)
        boxes = self.ocr(self.box_of_screen(0.2, 0.5, 0.3, 0.3, "精神改善剂检测区域"), re.compile(r'^可回复精神力'))
        if len(boxes) == 1:
            self.click_box(boxes[0], relative_y=-4)
            self.wait_click_box(
                lambda: self.ocr(self.right_button_zone, match='确认使用'))
            self.sleep(0.5)
            self.click_relative(0.95, 0.5)
            self.sleep(3)
            self.click_box(start_manxun)

    @property
    def right_button_zone(self):
        return self.box_of_screen(0.5, 0.6, 0.5, 0.3, "按钮检测区域")

    @property
    def top_right_button_zone(self):
        return self.box_of_screen(0.5, 0, 0.5, 0.2, "右上按钮检测区域")

    @property
    def bottom_button_zone(self):
        return self.box_of_screen(0.2, 0.8, 0.6, 0.2, "下面按钮检测区域")

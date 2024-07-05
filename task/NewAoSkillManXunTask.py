import re

from typing_extensions import override

from ok.feature.Box import find_box_by_name
from ok.task.TaskExecutor import FinishedException, TaskDisabledException
from task.NewManXunTask import NewManXunTask, find_index


class NewAoSkillManXunTask(NewManXunTask):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "循环漫巡凹技能"
        self.description = "烙痕使用上次编组, 只支持福利院"
        self.super_config = self.default_config
        self.default_config = {'角色名': '岑缨', '路线': '福利院', '支援烙痕': '于火光中', '支援烙痕类型': '专精',
                               '漫巡次数': 5,
                               '目标技能': ['职业联动', '针对打击', '奉献'], '目标技能个数': 3}
        self.default_config = {**self.default_config, **self.super_config}
        self.config_description["目标技能"] = "部分匹配, 中间带标点的，留半边，如'职业联动*菱形'，写'职业联动'"
        self.config_description["目标技能个数"] = "目标技能加起来一共刷多少个, 大于等于"
        self.config_description["漫巡次数"] = "刷多少次, 直到技能满足要求"
        self.config_description["支援烙痕"] = '部分匹配, 如"于火光中[蛋生]" 可以填"于火光中"'
        self.config_description["角色名"] = '部分匹配即可'
        self.config_description["路线"] = '只支持福利院'
        self.config_description["支援烙痕类型"] = '一定要匹配, 否则刷不到'
        self.config_type["支援烙痕类型"] = {'type': "drop_down", 'options': self.stats_seq}
        self.pause_combat_message = "成功刷到目标技能, 暂停"

    @override
    def run(self):
        self.log_info(f'run, config {self.config}')
        i = 0
        while True:
            i = i + 1
            if i > self.config.get('漫巡次数'):
                self.log_info(f'已经第{self.config.get("漫巡次数")}次，没刷到指定技能', notify=True)
                break
            self.info.clear()
            self.route = None
            self.info['目前漫巡次数'] = i
            self.log_info(f'凹技能进行第{self.info["目前漫巡次数"]} 次', notify=True)
            if not self.loop_manxun():
                break
        self.log_info("凹技能任务结束", notify=True)

    def confirm_generate(self):
        if self.info.get('已获得目标技能个数', 0) < self.config['目标技能个数']:
            return True

    def loop_manxun(self):
        is_main = self.check_is_main()
        if not is_main and not self.check_is_manxun_ui():
            boxes = self.ocr(box=self.box_of_screen(0.2, 0.5, width=0.8, height=0.3, name="漫巡路线检测区域"),
                             match=self.config['路线'])
            if boxes:
                self.route = boxes[0]
                self.log_debug(f'在漫巡路线选择界面 {self.route}')
            if not self.route:
                self.log_error("必须从主界面或漫巡界面开始", notify=True)
                self.screenshot("必须从主界面或漫巡界面开始")
                return False
        if is_main or self.route:
            if not self.enter_manxun():
                self.start_manxun()
            self.wait_click_ocr(0.42, 0.63, 0.62, 0.79, match='漫巡开始', time_out=60)
        while True:
            try:
                self.loop()
            except (FinishedException, TaskDisabledException):
                return True
            except Exception as e:
                self.screenshot(f"运行异常{e}")
                self.log_error(f"运行异常,已暂停:", e, True)
                self.pause()

    def start_manxun(self):
        boxes = self.ocr(box=self.bottom_button_zone)
        manxun_start = find_box_by_name(boxes, "漫巡开始")
        if not manxun_start:
            self.select_char()
            manxun_start = self.ocr(box=self.bottom_button_zone, match="漫巡开始")
        self.choose_assist_laohen()
        self.sleep(3)
        self.click_box(manxun_start)

    def if_skip_battle(self):
        if self.info.get('漫巡深度', 0) < self.config['深度等级最多提升到']:
            self.log_debug(f"未达到预定深度, 不跳过战斗")
            self.pause_combat_message = "未达到预定深度, 不跳过战斗"
            return False

        self.log_debug(f"检测技能是否满足条件 {self.info.get('已获得目标技能个数', 0)} {self.info.get('获得技能', [])}")
        if self.info.get('已获得目标技能个数', 0) >= self.config['目标技能个数']:
            self.pause_combat_message = "成功刷到目标技能, 暂停"
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
            self.info['已获取的目标技能'] = skills
            self.notification(f"已经获取到 {current_count}个目标技能 {skills}")
            if current_count >= self.config['目标技能个数']:
                self.pause()

    def select_char(self):
        char_name = self.wait_until(
            lambda: self.ocr(box=self.box_of_screen(0.4, 0.4, width=0.6, height=0.5, name="角色检测区域"),
                             match=re.compile(f"{self.config['角色名']}")),
            time_out=60,
            post_action=lambda: self.swipe_relative(0.8, 0.5, 0.5, 0.5, 1))
        if not char_name:
            raise Exception(f'找不到角色 {self.config["角色名"]}')
        self.click_box(char_name)
        next_step = self.wait_click_box(lambda: self.ocr(box=self.bottom_button_zone, match="下一步"))
        self.wait_click_box(lambda: self.ocr(box=self.top_right_button_zone, match="上次编队"))
        self.sleep(0.5)
        self.click_box(next_step)
        self.wait_click_box(lambda: self.ocr(box=self.top_right_button_zone, match="上次编组"))
        self.sleep(3)

    def choose_assist_laohen(self):
        boxes = self.ocr(box=self.box_of_screen(0.5, 0.5, width=0.5, height=0.5, name="支援记忆烙痕检测区域"),
                         match=re.compile("支援记忆烙痕"))
        zhiyuan = boxes[0]
        self.click_box(zhiyuan, relative_y=-0.5)
        self.sleep(2)
        assist_laohen_type = self.config.get("支援烙痕类型")
        laohen_type_index = find_index(assist_laohen_type, self.stats_seq)
        gap = self.height_of_screen((1564 - 1209) / 4 / 1080)
        laohen_type_y = self.height_of_screen(68 / 1080)
        laohen_type_x = self.screen_width - self.height_of_screen((1920 - 1564) / 1080) - (
                4 - laohen_type_index) * gap
        self.click(laohen_type_x, laohen_type_y)
        assist = self.wait_until(self.choose_assist_laohen_check,
                                 time_out=300,
                                 wait_until_before_delay=3,
                                 post_action=lambda: self.click_relative(0.91, 0.07))
        self.click_box(assist)
        self.sleep(2)
        select = self.ocr(box=self.box_of_screen(0.5, 0.5, width=0.5, height=0.5, name="支援记忆烙痕检测区域"),
                          match=re.compile("选择支援记忆烙痕"))
        if select:
            self.log_info("选了上次选中的支援烙痕, 再选一遍")
            self.choose_assist_laohen()

    def choose_assist_laohen_check(self):
        manpos = self.find_feature('manpo_90', 1, 1, 0.90)
        if manpos:
            boxes = self.ocr(box=self.box_of_screen(0.1, 0.3, width=0.9, height=0.6, name="支援烙痕检测区域"))
            for box_90 in manpos:
                laohen = box_90.find_closest_box('all', boxes,
                                                 lambda box: self.config.get('支援烙痕') in box.name)
                if laohen and box_90.closest_distance(laohen) < box_90.width * 2:
                    self.log_info(f"查找到满破烙痕 {laohen} {box_90}")
                    return box_90

    def enter_manxun(self):
        if not self.route:
            self.main_go_to_manxun()
            self.wait_click_box(
                lambda: self.ocr(box=self.box_of_screen(0.2, 0.5, width=0.8, height=0.3, name="漫巡路线检测区域"),
                                 match=self.config['路线']))
        else:
            self.click_box(self.route)
        go_manxun = self.wait_click_box(
            lambda: self.ocr(box=self.right_button_zone, match='前往回廊漫巡'))
        self.sleep(1)
        continue_manxun = self.ocr(box=self.dialog_zone, match='继续漫巡')
        if continue_manxun:
            self.click_box(continue_manxun)
            self.wait_click_box(
                lambda: self.ocr(box=self.dialog_zone, match='确认'))
            return True
        else:
            self.log_debug('start_manxun')
            # start_manxun = self.wait_click_box(
            #     lambda: self.ocr(box=self.star_combat_zone, match='开始新漫巡'), time_out=4)
            # self.sleep(1)
            boxes = self.ocr(box=self.box_of_screen(0.2, 0.5, width=0.3, height=0.3, name="精神改善剂检测区域"),
                             match=re.compile(r'^可回复精神力'))
            if len(boxes) == 1:
                self.click_box(boxes[0], relative_y=-4)
                self.wait_click_box(
                    lambda: self.ocr(box=self.right_button_zone, match='确认使用'))
                self.sleep(0.5)
                self.click_relative(0.95, 0.5)
                self.sleep(3)
                self.click_box(go_manxun)
            return False

    @property
    def right_button_zone(self):
        return self.box_of_screen(0.5, 0.6, width=0.5, height=0.3, name="按钮检测区域")

    @property
    def top_right_button_zone(self):
        return self.box_of_screen(0.5, 0, width=0.5, height=0.2, name="右上按钮检测区域")

    @property
    def bottom_button_zone(self):
        return self.box_of_screen(0.2, 0.8, width=0.6, height=0.2, name="下面按钮检测区域")

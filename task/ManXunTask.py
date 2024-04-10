import re

from typing_extensions import override

from ok.color.Color import calculate_color_percentage, white_color
from ok.feature.Box import find_box_by_name, find_boxes_by_name, find_boxes_within_boundary
from task.BJTask import BJTask


class ManXunTask(BJTask):

    def __init__(self):
        super().__init__()
        self.name = "自动漫巡任务"
        self.description = """自动漫巡
    """
        self.click_no_brainer = ["直接胜利", "属性提升", "前进", "通过", "继续", "收下", "跳过", "开始强化",
                                 re.compile(r"^解锁技能："), re.compile(r"^精神负荷降低"), "漫巡推进"]
        self.default_config = {
            "无法直接胜利, 自动投降跳过": False,
            "唤醒属性优先级": ["终端", "专精", "体质", "攻击", "防御"],
            "深度等级最多提升到": 12,
            "低深度选项优先级": ["风险区", "烙痕唤醒", "记忆强化", "高维同调", "研习区", "休整区"],
            "高深度选项优先级": ["风险区", "烙痕唤醒", "高维同调", "记忆强化", "研习区", "休整区"],
            "高低深度分界": 10,
            "跳过战斗": ["鱼叉将军-日光浅滩E"],
        }
        self.destination = None
        self.stats_up_re = re.compile(r"([\u4e00-\u9fff]+)\+(\d+)(?:~(\d+))?")

    def end(self, message, result=False):
        self.log_info(f"执行结束:{message}")
        return result

    @property
    def choice_zone(self):
        return self.box_of_screen(0.7, 0.25, 0.3, 0.5, "选项检测区域")

    @property
    def dialog_zone(self):
        return self.box_of_screen(0.25, 0.2, 0.5, 0.7, "弹窗检测区域")

    def filter_gaowei_number_zone(self, boxes):
        return self.box_of_screen(0.25, 0.5, 0.5, 0.5).in_boundary(boxes)

    @override
    def run_frame(self):
        if not self.check_is_manxun_ui():
            self.log_error("必须从漫巡选项界面开始, 并且开启路线追踪", notify=True)
            self.set_done()
        try:
            while self.loop():
                pass
        except Exception as e:
            self.log_error(f"运行异常:", e, True)

        self.log_info("自动漫巡任务结束", notify=True)
        self.set_done()

    def check_is_manxun_ui(self):
        choices = self.find_choices()
        if not choices:
            self.logger.debug("找不到选项")
            return False
        if self.find_depth() == 0:
            self.logger.debug("找不到深度")
            return False
        return choices

    def loop(self, choice=-1):
        choices, choice_clicked = self.click_choice(choice)
        if not choice_clicked:
            self.logger.error(f"没有选项可以点击")
            return False
        self.wait_until(lambda: self.do_handle_dialog(choice, choices, choice_clicked))
        if self.done:
            return False
        return True

    def do_handle_dialog(self, choice, choices, choice_clicked):
        boxes = self.ocr(self.dialog_zone)
        if self.find_depth(boxes) > 0:
            self.log_info(f"没有弹窗, 进行下一步")
            return True
        self.logger.debug(f"检测对话框区域 {boxes}")
        if find_box_by_name(boxes, "提升攻击"):
            box = self.find_highest_gaowei_number(boxes)
            self.click_box(box)
            self.log_info(f"高位同调 点击最高 {box}")
        elif confirm := find_box_by_name(boxes, "完成漫巡"):
            self.click_box(confirm)
            self.wait_click_box(lambda: self.ocr(self.dialog_zone, match="确认"))
            self.wait_click_box(lambda: self.ocr(self.star_combat_zone, match="跳过漫巡回顾"))
            self.wait_click_box(lambda: self.ocr(self.star_combat_zone, match="点击屏幕确认结算"))
            self.set_done()
        elif confirm := find_box_by_name(boxes, "解锁技能和区域"):
            self.handle_skill_dialog(boxes, confirm)
        elif find_box_by_name(boxes, "获得了一些技能点"):
            self.log_info(f"获取技能点成功")
            self.click_box(find_box_by_name(boxes, re.compile(r"^\+\d+")))
        elif keyin := find_box_by_name(boxes, "刻印技能上限"):
            keyin.y += keyin.height * 2.5
            keyin.x = self.width / 2 - keyin.width / 2
            self.draw_boxes("confirm_by_offset", keyin)
            self.log_info(f"区域技能,点击两次")
            self.click_box(keyin)
            self.sleep(0.5)
            self.click_box(keyin)
        elif stat_combat := find_box_by_name(boxes, "开始战斗"):
            skip_battle = find_box_by_name(boxes, self.config.get("跳过战斗"))
            self.logger.debug(
                f"开始战斗 跳过战斗查询结果:{skip_battle} abs(choice):{abs(choice)} len(choices) {len(choices)}")
            if skip_battle and abs(choice) < len(choices):
                self.log_info(f"回避配置列表里的战斗 {skip_battle}")
                self.click_cancel()
                return self.loop(choice=choice - 1)
            elif self.config.get("无法直接胜利, 自动投降跳过"):
                self.log_info(f"开始自动跳过战斗")
                self.click_box(stat_combat)
                self.auto_skip_combat()
            else:
                message = "未开启自动战斗, 无法继续漫巡, 暂停中, 请手动完成战斗或开启自动跳过后继续"
                self.log_info(message, True)
                self.pause()
        elif no_brain_box := self.click_box_if_name_match(boxes, self.click_no_brainer):
            self.log_info(f"点击固定对话框: {no_brain_box.name}")
        elif stats_up_choices := self.find_stats_up(boxes):
            self.handle_stats_up(stats_up_choices)
        else:
            raise RuntimeError(f"未知弹窗 无法处理")
        return True

    def find_stats_up(self, boxes):
        for box in boxes:
            if re.search(r"^[\u4e00-\u9fa5]{2}$", box.name):
                closest = box.find_closest_box("right", boxes)
                if closest is not None:
                    distance = closest.closest_distance(box)
                    if distance < box.width:
                        match = re.search(r"\+(\d+)(?:~(\d+))?", closest.name)
                        if match:
                            box.name += match.group(0)
                            self.logger.debug(f"合并较近属性和数值, {box} {closest.name}")
                            closest.name = ""

        return find_boxes_by_name(boxes, self.stats_up_re)

    def auto_skip_combat(self):
        start_combat = self.wait_until(lambda: self.ocr(self.star_combat_zone, "开始战斗"), time_out=50)
        if not start_combat:
            raise RuntimeError("无法找到开始战斗按钮")
        self.click_relative(0.04, 0.065)
        self.wait_click_box(lambda: self.ocr(self.dialog_zone, "离开战斗"))
        self.wait_click_box(lambda: self.ocr(self.dialog_zone, "离开战斗"))
        self.wait_click_box(lambda: self.ocr(self.dialog_zone, "继续"), time_out=30)
        self.wait_click_box(lambda: self.ocr(self.dialog_zone, match=re.compile(r"回避")))
        self.wait_click_box(lambda: self.ocr(self.dialog_zone, match=re.compile(r"确\s?认")))

    def handle_stats_up(self, stats_up_choices):
        stats_up_parsed = self.parse_stats_choices(stats_up_choices)
        target = list(stats_up_parsed.values())[0][0][1]
        for stat in self.config['唤醒属性优先级']:
            if stat in stats_up_parsed:
                # Assuming stats_up_parsed[stat] is a list of tuples (value, box)
                # and we want the one with the highest 'value'
                value, box = max(stats_up_parsed[stat], key=lambda x: x[0])
                self.log_info(f"查找最高优先级提升属性结果 {box.name}")
                target = box
                break
        self.log_info(
            f"选择升级属性 {stats_up_choices} stats_up_parsed:{stats_up_parsed} target:{target}")
        self.click_box(target)

    def handle_skill_dialog(self, boxes, confirm):
        search_skill_name_box = confirm.copy(-confirm.width / 2, -confirm.height * 2, confirm.width,
                                             confirm.height * 0.7)
        self.draw_boxes("skill_search_area", search_skill_name_box)
        skills = find_boxes_within_boundary(boxes, search_skill_name_box)
        self.draw_boxes("skills", skills)
        self.info_add_to_list("获得技能", [obj.name for obj in skills])
        self.log_info(f"获取技能 {skills}")
        self.click_box(confirm)

    def click_choice(self, index=-1):
        choices = self.find_choices()
        if choices is None:
            return None, None
        if abs(index) > len(choices):
            raise ValueError(f"click_choice out of bonds")
        else:
            priority = self.config['低深度选项优先级'] if self.info.get('漫巡深度', 0) < self.config[
                '高低深度分界'] else \
                self.config[
                    '高深度选项优先级']
            if choices[index].name == "深度等级提升":
                depth = self.find_depth()
                self.log_info(f"提升深度, {depth} 目前是第{abs(index)}个选项, 共有{len(choices)}选项")
                if depth < self.config['深度等级最多提升到'] or abs(index) == len(choices):
                    self.log_info(f"提升深度,当前深度{depth}")
                else:
                    self.log_info(f"不提升深度,当前深度{depth}")
                    index -= 1
                    index = find_priority_string(choices, priority, index)
            else:
                index = find_priority_string(choices, priority, index)
            self.click_box(choices[index])
            self.log_info(
                f"点击选项:{choices[index]}, 使用优先级 {priority}, index {index}, {choices}")
        return choices, choices[index]

    def do_find_choices(self):
        boxes = self.ocr(self.choice_zone)
        choices = find_boxes_by_name(boxes, re.compile(r"^通往"))
        if len(choices) > 0:
            for i in range(len(choices)):
                if self.destination is None:
                    self.logger.debug(f"检测到追踪目标: {choices[i].name}")
                    self.destination = choices[i].name
                choices[i].height *= 3
                if self.destination != choices[i].name:
                    self.log_info("排除错误追踪目标")
                    del choices[i]
                    continue
                right_text_box = choices[i].find_closest_box("down", boxes, self.is_black_text)
                if right_text_box is not None:
                    choices[i].name = right_text_box.name
                    boxes.remove(right_text_box)
        else:
            choices = find_boxes_by_name(boxes, "风险区")
        self.logger.debug(f"检测选项区域结果: {choices}")
        return choices

    def find_choices(self):
        return self.wait_until(self.do_find_choices, time_out=10)

    def find_depth(self, boxes=None):
        if boxes is None:
            boxes = self.ocr(self.dialog_zone)
        depth_box = None
        depth = 0
        numbers = find_boxes_by_name(boxes, re.compile(r"^[01D][0-9]$"))
        for number in numbers:
            # 居中大字深度
            if self.box_in_horizontal_center(number, off_percent=0.8) and number.height / self.height > 0.07:
                depth_box = number
                break
        if depth_box is not None:
            depth_box.name = depth_box.name.replace("D", "2")
            depth = int(depth_box.name)
            self.info['漫巡深度'] = depth
        return depth

    def click_cancel(self):
        self.click_relative(0.5, 0.1)

    def find_highest_gaowei_number(self, boxes):
        boxes = self.filter_gaowei_number_zone(boxes)
        highest_gaowei_number = 0
        highest_gaowei_box = None
        # 文字转数字
        for box in boxes:
            if isinstance(box.name, str) and box.name[0] == '+' and all(
                    char.isdigit() or char == '-' or char == '+' or char == ' ' for char in box.name):
                box.name = box.name.replace('-', '')
                # Split the string by '+' and sum the numbers
                numbers = box.name.split('+')
                sum_gaowei = sum(int(number) for number in numbers if number)
                box.name = sum_gaowei

        # 合并右边的数值,并把右边的改为0
        for box in boxes:
            if isinstance(box.name, int) and box.name > 0:
                right_closest = box.find_closest_box("right", boxes)
                if right_closest is not None:
                    distance = box.closest_distance(right_closest)
                    if distance < box.width / 2 and isinstance(right_closest.name, int):
                        self.log_debug(f"sum_gaowei add right {box.name} += {right_closest.name}")
                        box.name = box.name + right_closest.name
                        right_closest.name = 0
                weight = find_text_color_weight(self.frame, box)
                self.log_debug(f"sum_gaowei * weight {sum_gaowei} = {weight} x {box.name}")
                box.name = weight * box.name
                if box.name > highest_gaowei_number:
                    highest_gaowei_number = box.name
                    highest_gaowei_box = box
        self.draw_boxes("ocr", boxes)
        return highest_gaowei_box

    def parse_stats_choices(self, boxes):
        attributes = {}
        for box in boxes:
            # Find all matches of the pattern in the input string
            for match in re.finditer(self.stats_up_re, box.name):
                attribute, start, end = match.groups()
                # Calculate the value. If 'end' is None, use 'start'; otherwise, calculate the average.
                value = int(start) if not end else (int(start) + int(end)) / 2
                a_list = attributes.get(attribute, [])
                a_list.append((value, box))
                attributes[attribute] = a_list

        return attributes

    def is_black_text(self, box):
        black_percentage = calculate_color_percentage(self.frame, black_color, box)
        return black_percentage >= 0.05


def find_priority_string(input_list, priority_list, start_index=-1):
    # 不在priority_list 为最高优先级
    for i in range(start_index, -len(input_list) - 1, -1):
        if input_list[i].name not in priority_list:
            return i
    for priority in priority_list:
        for i in range(start_index, -len(input_list) - 1, -1):
            # If the current string is in the priority list
            if priority == input_list[i].name:
                # Return the negative index of the string in the input list
                return i
    return start_index


def find_text_color_weight(image, box):
    green_percentage = calculate_color_percentage(image, green_color, box)
    if green_percentage > 0.07:  # 绿色是点亮, 优先
        return 2
    yellow_percentage = calculate_color_percentage(image, yellow_color, box)
    if yellow_percentage > 0.07:  # 黄色是1000+ 乘以1.5
        return 3
    white_percentage = calculate_color_percentage(image, white_color, box)
    if white_percentage > 0.07:
        return 1
    return 0


green_color = {
    'r': (132, 152),  # Red range
    'g': (222, 242),  # Green range
    'b': (166, 186)  # Blue range
}

black_color = {
    'r': (0, 25),  # Red range
    'g': (0, 25),  # Green range
    'b': (0, 25)  # Blue range
}

yellow_color = {
    'r': (230, 250),  # Red range
    'g': (220, 240),  # Green range
    'b': (130, 150)  # Blue range
}

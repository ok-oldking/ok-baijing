import re

from typing_extensions import override

from ok.color.Color import calculate_color_percentage
from ok.feature.Box import find_box_by_name, find_boxes_by_name, find_boxes_within_boundary, average_width
from ok.task.TaskExecutor import FinishedException, TaskDisabledException
from task.BJTask import BJTask


def get_current_stats(s):
    try:
        # Split the string on '/'
        parts = s.split('/')
        # Check if there are exactly two parts and both are digits
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0])
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class NewManXunTask(BJTask):

    def __init__(self):
        super().__init__()
        self.update_stats_queue = None
        self.name = "执行一次自动漫巡"
        self.description = """自动漫巡, 必须进入漫巡后开始, 并开启追踪
    """
        self.click_no_brainer = ["直接胜利", "属性提升", re.compile(r"^前进"), "通过", "继续", "收下", "跳过",
                                 "开始强化",
                                 re.compile(r"^解锁技能："), re.compile(r"^精神负荷降低"), "漫巡推进"]
        self.default_config = {
            "深度等级最多提升到": 12,
            "低深度选项优先级": ["属性平台", "技能平台"],
            "高深度选项优先级": ["技能平台", "属性平台"],
            "高低深度分界": 6,
            "属性优先级": ["专精", "攻击", "终端", "防御", "体质", "技能点"],
            # "终端900上限": False,
            "烙痕唤醒黑名单": ["幕影重重", "谎言之下", "馆中遗影"],
            # "跳过战斗": ["鱼叉将军-日光浅滩E"],
            # "烙痕属性提升不选技能点": True,
            "自定义路径": ["3-01|[技能平台,属性平台]|2", "3-02|[技能平台,属性平台]|2", "3-04|[技能平台,属性平台]|1"]
        }
        self.config_description = {
            "投降跳过战斗": "如果无法直接胜利, 自动投降跳过",
            "深度等级最多提升到": "海底图建议12",
            "高低深度分界": "比如可以配置低深度优先记忆强化, 高深度优先高维同调",
            "烙痕唤醒黑名单": "可以使用烙痕名称或者核心技能名称, 部分匹配即可",
            "跳过战斗": "不打的战斗, 比如鱼叉将军",
            "烙痕唤醒属性优先级": "比如用烙痕凑900终端",
            "自定义路径": "使用半角符号，格式为 区域|[选项1名称,选项2名称]|选第几个。"
        }
        self.stats_up_re = re.compile(r"([\u4e00-\u9fff]+)\+(\d+)(?:~(\d+))?")
        self.pause_combat_message = "未开启自动战斗, 无法继续漫巡, 暂停中, 请手动完成战斗或开启自动跳过后继续"
        self.stats_seq = ["体质", "防御", "攻击", "专精", "终端"]
        self.update_stats_thread = None
        self.ocr_target_height = 700  # 缩小图片提升ocr速度
        self.total_anjiao_count = 3  # 预测暗礁属性
        self.custom_routes = []
        self.to_update_stats = True

    def on_create(self):
        self.log_debug('on_create')

    @property
    def zhongduan_max(self):
        return 900 if self.config.get("终端900上限") else 1250

    def validate_config(self, key, value):
        self.custom_routes.clear()
        if key == '自定义路径':
            for v in value:
                try:
                    zone, choices, to_choose = v.split('|')
                    list_of_choices = choices[1:-1].split(',')
                    config_list = [zone, list_of_choices, int(to_choose)]
                    if len(config_list) != 3:
                        return f'自定义路径配置格式错误:{v}'
                    self.custom_routes.append(config_list)
                except Exception as e:
                    self.log_error(f'自定义路径 配置错误：{v}', exception=e)
                    return f'自定义路径配置格式错误:{v}'
            self.log_info(f'加载自定义路径:{self.custom_routes}')

    def end(self, message, result=False):
        self.log_info(f"执行结束:{message}")
        return result

    @property
    def choice_zone(self):
        return self.box_of_screen(0.76, 0.50, 0.91, 0.83, name="选项检测区域")

    @property
    def current_zone(self):
        return self.box_of_screen(0.6, 0.8, width=0.3, height=0.2, name="当前区域")

    @property
    def stats_zone(self):
        return self.box_of_screen(0.28, 0.92, 0.73, 0.98, name="当前属性区域")

    @property
    def dialog_zone(self):
        return self.box_of_screen(0.05, 0.24, 0.92, 0.87, name="弹窗检测区域")

    @property
    def battle_popup_zone(self):
        return self.box_of_screen(0.25, 0.15, width=0.5, height=0.85, name="战斗检测区域")

    def filter_gaowei_number_zone(self, boxes):
        return self.box_of_screen(0.25, 0.5, width=0.5, height=0.5).in_boundary(boxes)

    @override
    def run(self):
        self.log_info(f'run, config {self.config}')
        if not self.check_is_manxun_ui():
            self.log_error("必须选好角色进入漫巡界面后开始, 并且开启路线追踪", notify=True)
            self.screenshot("必须选好角色进入漫巡界面后开始")
            return
        while True:
            try:
                self.loop()
            except FinishedException:
                self.log_info("自动漫巡任务结束", notify=True)
                return
            except TaskDisabledException:
                self.log_info("点击停止", notify=True)
                return
            except Exception as e:
                self.screenshot(f"运行异常{e}")
                self.log_error(f"运行异常,已暂停:", e, True)
                self.pause()

    def check_is_manxun_ui(self):
        if self.ocr_zone():
            return True
        try:
            return self.do_handle_dialog(-1)
        except Exception as e:
            self.log_error(f'check_is_manxun_ui handle dialog failed', e)

    def loop(self, choice=-1):
        choices, choice_clicked = self.click_choice(choice)
        if not choice_clicked:
            self.logger.error(f"没有选项可以点击, 请确认是否开启漫巡设置全部简化！")
            self.screenshot("没有选项可以点击")
            return self.handle_dialog_with_retry(choice)
        self.wait_until(lambda: self.handle_dialog_with_retry(choice), wait_until_before_delay=1.5)

    def handle_dialog_with_retry(self, choice):
        for i in range(2):
            try:
                self.do_handle_dialog(choice)
                self.sleep(0.5)
                return True
            except FinishedException as e:
                raise e
            except Exception as e:
                if i == 0:
                    self.screenshot("处理对话框异常重试一次")
                    self.log_error("处理对话框异常 重试一次", e)
                    self.sleep(5)
                    continue
                else:
                    raise e

    def stats_priority(self, gaowei):
        return self.config['属性优先级']

    def update_current_stats(self):
        if self.to_update_stats:
            self.handler.post(lambda: self.do_update_current_stats(self.frame))

    def do_update_current_stats(self, frame):
        # if frame is None:
        #     self.log_info("No frame in queue, destroyed")
        #     return
        # self.ocr_stats(frame)
        pass

    def ocr_stats(self, frame=None):
        boxes = self.ocr(box=self.stats_zone, match=re.compile(r'^[1-9]\d*$'), frame=frame)
        if len(boxes) != 5:
            # self.log_error(f"无法找到5个属性, {boxes}")
            return False
        else:
            stats = [int(box.name) for box in boxes]
            self.update_stats_for_anjiao(stats)
            self.info['当前属性'] = stats
            self.log_debug(f"ocr_stats {stats}")
            return True

    def update_stats_for_anjiao(self, stats):
        missing_count = self.total_anjiao_count - self.info.get('暗礁次数', 0)
        if missing_count > 2:
            missing_count = 2
        for _ in range(missing_count):
            sorted_indexes = target_index_array(stats)
            for i, sort in enumerate(sorted_indexes):
                if sort < 2:  # 最低两个加75
                    stats[i] += 75
                elif sort < 3:
                    stats[i] += 40
                else:
                    stats[i] += 10

    def do_handle_dialog(self, choice):
        boxes = self.ocr(box=self.dialog_zone)
        choices = self.do_find_choices()
        if choices is not True and len(choices) > 0:
            self.log_info(f"没有弹窗, 进行下一步")
            return False
        self.logger.debug(f"检测对话框区域 {boxes}")
        ups = find_boxes_by_name(boxes, "提升")
        if huanxing := find_boxes_by_name(boxes, '烙痕唤醒'):
            self.try_handle_laohen_choices(huanxing, boxes)
        elif depth_ups := find_boxes_by_name(boxes, ["维持当前深度", "提升深度到", "降低深度到"]):
            levels = []
            for depth in depth_ups:
                levels.append(int(depth.find_closest_box('right', boxes).name))
            self.log_debug(f'depth levels {levels}')
            for reverse_index, value in enumerate(reversed(levels)):
                original_index = len(levels) - 1 - reverse_index
                if value <= self.config.get('深度等级最多提升到', 12):
                    self.click_box(depth_ups[original_index])
                    self.log_info(f'点击等级提升 {value} {depth_ups[original_index]}')
                    self.info['漫巡深度'] = value
                    break
            self.click_box(depth_ups[0])
        elif confirm := find_box_by_name(boxes, "完成漫巡"):
            self.click_box(confirm)
            self.wait_click_box(lambda: self.ocr(box=self.dialog_zone, match="确认"))
            self.wait_click_box(lambda: self.ocr(box=self.star_combat_zone, match="跳过漫巡回顾"))
            self.wait_click_box(lambda: self.ocr(box=self.star_combat_zone, match="点击屏幕确认结算"))
            if self.confirm_generate():
                self.wait_click_box(
                    lambda: self.ocr(box=self.box_of_screen(0.7, 0.6, width=0.3, height=0.4), match="确认生成"))
                self.wait_click_box(lambda: self.ocr(box=self.dialog_zone, match="完成漫巡"))
                self.wait_click_box(
                    lambda: self.ocr(box=self.box_of_screen(0.5, 0.5, width=0.4, height=0.3), match="确定完成"))
                self.wait_until(lambda: self.ocr(box=self.box_of_screen(0, 0, width=0.2, height=0.2)),
                                pre_action=lambda: self.click_relative(0.5, 0.1), time_out=90)
            raise FinishedException()
        elif len(ups) > 1:
            stats = []
            for up in ups:
                stats.append(remove_non_digits_and_convert(up.find_closest_box('up', boxes).name))
            self.log_info(f'高位同调选项: {stats}')
            max_value = max(stats)
            max_index = stats.index(max_value)
            self.click_box(ups[max_index])
            self.log_info(f"高位同调 点击最高 {ups[max_index]} {stats[max_index]}")
            self.to_update_stats = True
        elif weichi_huibi := find_box_by_name(boxes, re.compile('^维持深度回避')):
            self.log_info('维持深度回避')
            self.click_box(weichi_huibi)
        elif kaizhan := find_box_by_name(boxes, re.compile('^开战')):
            if avoid := find_box_by_name('维持当前深度回避', boxes):
                self.click_box(avoid)
                self.log_info('wait 维持当前深度 ocr done')
            else:
                self.log_info('点击开战')
                self.click_box(kaizhan)
                self.wait_ocr(box=self.dialog_zone, match=re.compile("深度"), time_out=60)
            self.do_handle_dialog(choice)
        elif confirm := find_boxes_by_name(boxes, "技能获取"):
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
        elif start_combat := find_box_by_name(boxes, "开始战斗"):
            self.click_box(start_combat)
            self.logger.debug(
                f"开始战斗 自动战斗")
            self.auto_combat()
        elif no_brain_boxes := find_boxes_by_name(boxes, self.click_no_brainer):
            no_brain_box = no_brain_boxes[-1]
            self.click_box(no_brain_box)
            if no_brain_box.name == '属性提升':
                self.log_info('暗礁属性提升')
                self.info_add('暗礁次数')
                self.to_update_stats = True
            elif no_brain_box.name == '漫巡推进' or no_brain_box.name == '前进':
                self.sleep(4)
                self.ocr_zone()
            else:
                self.log_info(f"点击固定对话框: {no_brain_box.name}")
        elif stats_up_choices := self.find_stats_up(boxes):
            self.handle_stats_up(stats_up_choices)
            self.to_update_stats = True
        else:
            raise Exception(f"未知弹窗 无法处理")
        return True

    def ocr_zone(self):
        zone = self.ocr(box=self.box_of_screen(0.09, 0.11, 0.18, 0.15))
        self.log_debug(f'ocr zone {zone}')
        if zone:
            if '浮世' not in zone[0].name:
                return False
            self.info['当前区域'] = zone[0].name
            self.log_info(f'当前区域 {self.info["当前区域"]}')
            return self.info['当前区域']

    def confirm_generate(self):
        return False

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

    def auto_combat(self):
        self.log_info('开始查找开始战斗')
        start_combat = self.wait_ocr(box=self.star_combat_zone, match="开始战斗", time_out=180, raise_if_not_found=True)
        self.sleep(2)
        self.log_info('点击开始战斗')
        self.click_box(start_combat)
        self.wait_until(self.ocr_zone, time_out=300)
        # self.wait_click_ocr(box=self.star_combat_zone, match="开始战斗", time_out=300, raise_if_not_found=True)
        # self.click_relative(0.04, 0.065)
        # self.sleep(100)
        # self.wait_click_box(lambda: self.ocr(box=self.battle_popup_zone, match="离开战斗"))
        # self.wait_click_box(lambda: self.ocr(box=self.battle_popup_zone, match="离开战斗"))
        # self.wait_click_box(lambda: self.ocr(box=self.dialog_zone, match="继续"), time_out=30)
        # self.wait_click_box(lambda: self.ocr(box=self.dialog_zone, match=re.compile(r"回避")))
        # self.wait_click_box(lambda: self.ocr(box=self.dialog_zone, match=re.compile(r"确\s?认")))

    def handle_stats_up(self, stats_up_choices):
        stats_up_parsed = self.parse_stats_choices(stats_up_choices)
        skilled_list = []
        target = None
        priority = self.stats_priority(False)
        for stat in priority:
            if target is not None:
                break
            for box_stat, _, box in stats_up_parsed:
                if box_stat == stat:
                    target = box
                    break
        if target is None:
            if skilled_list:
                target = skilled_list[0]
            else:
                target = stats_up_parsed[0][2]
        self.log_info(
            f"选择升级属性 {stats_up_choices} stats_up_parsed:{stats_up_parsed} target:{target} priority:{priority} skilled_list:{skilled_list}")
        if target:
            self.click_box(target)
            return True

    def handle_skill_dialog(self, boxes, confirm):
        confirm = confirm[-1]
        search_skill_name_box = confirm.copy(-confirm.width / 2, -confirm.height * 2, confirm.width,
                                             confirm.height * 0.7)
        self.draw_boxes("skill_search_area", search_skill_name_box)
        skills = find_boxes_within_boundary(boxes, search_skill_name_box)
        self.draw_boxes("skills", skills)
        self.info_add_to_list("获得技能", [obj.name for obj in skills])
        self.check_skills()
        self.log_info(f"获取技能 {skills}")
        self.click_box(confirm)
        self.sleep(4)
        self.ocr_zone()

    def check_skills(self):
        pass

    def check_custom_route(self, choices):
        for custom_route in self.custom_routes:
            zone, custom_choices, custom_index = custom_route
            zone_match = (zone in self.info.get('当前区域', []))
            size_custom = len(custom_choices)
            self.log_debug(
                f'check_custom_route {choices} 当前区域:{self.info.get("当前区域")} {zone_match} {size_custom}')
            if zone_match:
                if size_custom == len(choices):
                    all_match = True
                    for i in range(size_custom):
                        if custom_choices[i] not in choices[i].name:
                            all_match = False
                            break
                    if all_match:
                        index = custom_index - 1
                        self.log_info(f"自定义路径找到，{custom_route} 点击第{custom_index}个 {choices[index]}")
                        self.click_box(choices[index])
                        return True, choices[index]
        return False, None

    def click_choice(self, index=-1):
        choices = self.find_choices()
        if choices is True:
            self.log_debug(f'choices in bg try handle dialog again')
            return None, None
        if choices is None:
            return None, None
        if abs(index) > len(choices):
            raise ValueError(f"click_choice out of bonds")
        else:
            handled, clicked = self.check_custom_route(choices)
            if handled:
                return choices, clicked
            else:
                priority = self.config['低深度选项优先级'] if self.info.get('漫巡深度', 0) < self.config[
                    '高低深度分界'] else \
                    self.config[
                        '高深度选项优先级']
                index = find_priority_string(choices, priority, index)
            self.update_current_stats()
            self.click_box(choices[index])
            self.log_info(
                f"点击选项:{choices[index]}, 使用优先级 {priority}, index {index}, {choices}")
        return choices, choices[index]

    def try_handle_laohen_choices(self, huanxing, boxes):
        stats_up_choices = self.find_stats_up(boxes)
        if stats_up_choices and self.handle_stats_up(stats_up_choices):
            return
        target = huanxing[0]
        if len(huanxing) == 2:
            black_list = [re.compile(s) for s in self.config["烙痕唤醒黑名单"]] + [re.compile("核心技能已解锁满级")]
            blacks = find_boxes_by_name(boxes, black_list)
            for black in blacks:
                if black.x < self.width_of_screen(0.5):
                    target = huanxing[1]
                    self.log_debug(f'烙痕唤醒 黑名单 {black}')
                else:
                    target = huanxing[0]
        if target.x < self.width_of_screen(0.5):
            self.log_info('点击右边唤醒')
            self.click_relative(0.27, 0.71)
        else:
            self.click_relative(0.75, 0.71)
            self.log_info('点击左边唤醒')

    def do_find_choices(self):
        choices = self.ocr(box=self.choice_zone)
        for i in range(len(choices) - 1, -1, -1):
            percent = calculate_color_percentage(self.frame, text_white_color, box=choices[i])
            if percent < 0.02 or percent > 0.3:
                self.log_debug(f'choice is not in foreground {percent}, remove  {choices[i]}')
                del choices[i]
                return True
        # if len(choices) == 1:
        #     self.info['追踪目标'] = choices[0].name
        # if len(choices) > 0:
        #     for i in range(len(choices)):
        #         if self.info.get('追踪目标') is None:
        #             self.logger.debug(f"检测到追踪目标: {choices[i].name}")
        #             self.info['追踪目标'] = choices[i].name
        #         choices[i].height *= 3
        #         if self.info.get('追踪目标') != choices[i].name:
        #             self.log_info("排除错误追踪目标")
        #             del choices[i]
        #             continue
        #         right_text_box = next((x for x in boxes if self.is_black_text(x)), None)
        #         if right_text_box is not None:
        #             choices[i].name = right_text_box.name
        #             boxes.remove(right_text_box)
        # else:
        #     choices = find_boxes_by_name(boxes, "风险区")
        self.logger.debug(f"检测选项区域结果: {choices}")
        return choices

    def find_choices(self):
        return self.wait_until(self.do_find_choices, time_out=10)

    def find_depth(self, boxes=None):
        if boxes is None:
            boxes = self.ocr(box=self.dialog_zone)
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
        elif find_box_by_name(boxes, "深度等级") is not None:  # 弹窗可能出现太快 无法找到depth_box, 有深度等级的话就继续
            depth = self.info.get('漫巡深度', 0)
        return depth

    def click_cancel(self):
        self.click_relative(0.5, 0.1)

    def find_highest_gaowei_number(self, boxes):
        boxes = self.filter_gaowei_number_zone(boxes)
        # 文字转数字
        current_stats = []
        for box in boxes:
            if stats := get_current_stats(box.name):
                current_stats.append(stats)
        if len(current_stats) != 5:
            self.log_error(f"没有找到五个属性 {current_stats}")
            current_stats = self.info.get('当前属性', [0, 0, 0, 0, 0])
        else:
            self.update_stats_for_anjiao(current_stats)
            self.info['当前属性'] = current_stats
        tisheng_boxes = find_boxes_by_name(boxes, re.compile(r"^提升"))
        if len(tisheng_boxes) != 5:
            raise Exception("没有找到五个提升")
        avg_width = average_width(tisheng_boxes)
        self.log_debug(f"高维:目前数值 {current_stats} {tisheng_boxes}")
        highest_priority = -2
        highest_index = 0
        stats_priority = self.stats_priority(True)
        for i in range(5):
            box, yellow_line, gray_line = self.locate_gaowei_line(tisheng_boxes[i], avg_width)
            if current_stats[i] >= 1000:
                yellow_line = yellow_line / 2
            if gray_line == 0:  # 全点亮或者没有对应卡
                if yellow_line > 0:  # 全点亮 以黄线数量为优先级
                    priority = 1000 * yellow_line
                else:  # 没对应卡 最低优先级
                    priority = -1
            else:  # 有灰色线, 以黄线数量为优先级
                priority = 100 * yellow_line
            stats_priority_index = find_index(tisheng_boxes[i].name.replace('提升', ''), stats_priority)
            if stats_priority_index != -1:
                priority += 10 - stats_priority_index
            if current_stats[i] >= 1280 or (i == 4 and current_stats[i] >= self.zhongduan_max):  ##超过上限或者终端超过900不点
                priority = -1
            if priority > highest_priority:
                highest_index = i
                highest_priority = priority
            self.log_debug(f"高维属性 {box} {yellow_line} {gray_line}  {priority}")
        self.log_debug(f"最高优先级 高维 {tisheng_boxes[highest_index]} {highest_priority} {stats_priority}")
        self.draw_boxes("ocr", boxes)
        return tisheng_boxes[highest_index]

    def locate_gaowei_line(self, box, width):
        box = box.copy(height_offset=-box.height * 0.8,
                       name=f"{box.name}_search_line")
        box.width = width
        box.y = self.height_of_screen(0.592)
        gray_percentage = calculate_color_percentage(self.frame, gray_color, box) * 100
        yellow_percentage = calculate_color_percentage(self.frame, yellow_color, box) * 100
        gray_line = (gray_percentage + gray_percent_per_line / 2) / gray_percent_per_line
        yellow_line = (yellow_percentage + yellow_percent_per_line / 2) / yellow_percent_per_line
        # self.log_debug(f"高维点亮 {box} {yellow_line} {yellow_percentage} {yellow_percent_per_line}")
        self.draw_boxes(boxes=box, color="blue")
        return box, int(yellow_line), int(gray_line)

    # 寻找灰色, 如有则降低优先级

    def parse_stats_choices(self, boxes):
        stats_list = []
        for box in boxes:
            # Find all matches of the pattern in the input string
            for match in re.finditer(self.stats_up_re, box.name):
                attribute, start, end = match.groups()
                # Calculate the value. If 'end' is None, use 'start'; otherwise, calculate the average.
                value = int(start) if not end else (int(start) + int(end)) / 2
                stats_list.append((attribute, value, box))

        return sorted(stats_list, key=lambda x: x[1], reverse=True)

    def is_black_text(self, box):
        black_percentage = calculate_color_percentage(self.frame, black_color, box)
        return black_percentage >= 0.02


def find_priority_string(input_list, priority_list, start_index=-1):
    # 不在priority_list 为最高优先级
    for i in range(start_index, -len(input_list) - 1, -1):
        in_list = False
        for priority in priority_list:
            if priority in input_list[i].name:
                in_list = True
        if not in_list:
            return i
    for priority in priority_list:
        for i in range(start_index, -len(input_list) - 1, -1):
            # If the current string is in the priority list
            if priority in input_list[i].name:
                # Return the negative index of the string in the input list
                return i
    return start_index


def find_index(element, lst):
    try:
        return lst.index(element)
    except ValueError:
        return -1


def remove_item(original_list, items_to_remove):
    if items_to_remove:
        return [item for item in original_list if item not in items_to_remove]
    else:
        return original_list


def target_index_array(lst):
    # Pair each element with its index and sort by the element, then by the original index
    sorted_pairs = sorted((e, i) for i, e in enumerate(lst))

    # Create a list to hold the target indices
    target_indices = [-1] * len(lst)

    # Assign continuous indices to the elements in the sorted list
    current_index = 0
    for _, original_index in sorted_pairs:
        if target_indices[original_index] == -1:
            target_indices[original_index] = current_index
            current_index += 1
        else:
            # If the number is equal to the previous, increment the current index
            current_index += 1
            target_indices[original_index] = current_index

    return target_indices


def remove_non_digits_and_convert(s):
    # Use regular expression to keep only digits and '+' characters
    clean_string = re.sub(r'[^0-9+]', '', s)
    clean_string = clean_string.strip('+')
    # Evaluate the cleaned string as a mathematical expression
    try:
        return eval(clean_string)
    except Exception as e:
        return 0


gray_percent_per_line = 0.03660270078 * 100
yellow_percent_per_line = 0.02821869488 * 100

green_color = {
    'r': (132, 152),  # Red range
    'g': (222, 242),  # Green range
    'b': (166, 186)  # Blue range
}

black_color = {
    'r': (0, 30),  # Red range
    'g': (0, 30),  # Green range
    'b': (0, 30)  # Blue range
}

gray_color = {
    'r': (80, 105),  # Red range
    'g': (90, 110),  # Green range
    'b': (97, 120)  # Blue range
}

yellow_color = {
    'r': (220, 250),  # Red range
    'g': (180, 210),  # Green range
    'b': (90, 110)  # Blue range
}
text_white_color = {
    'r': (240, 255),  # Red range
    'g': (240, 255),  # Green range
    'b': (240, 255)  # Blue range
}

import random
import re

from ok.color.Color import calculate_color_percentage
from task.BJTask import BJTask


class DailyTask(BJTask):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "一键收菜清日常(最好用模拟器)"
        self.description = "打开模拟器，启动游戏，签到，进入主页, 刷日常"
        self.default_config = {"免费购物": True, "刷体力总开关": True, "随机刷材料次数": 3,
                               "随机刷技能书次数": 3, "喝茶3次": True, "友情点": True,
                               "收菜": True, "免费召唤烙痕": True, "升级烙痕": True, "领任务奖励": True
                               }
        self.config_description = {
            "随机刷技能书次数": "每次40体",
            "随机刷材料次数": "每次40体"
        }
        self.info['使用体力药'] = 0

    def run(self):
        if self.ensure_main_page():
            self.log_info("进入游戏主页成功！", True)
        else:
            self.log_error("进入游戏主页失败！", notify=True)
            return
        if self.config.get("刷体力总开关") and (
                self.config.get('随机刷材料次数') > 0 or self.config.get('随机刷技能书次数') > 0):
            self.combat()
        if self.config.get("喝茶3次"):
            self.hecha()
        if self.config.get("友情点"):
            self.friends()
        if self.config.get("收菜"):
            self.shoucai()
        if self.config.get("免费购物"):
            self.go_shopping()
        if self.config.get("免费召唤烙痕"):
            self.free_summon()
        if self.config.get("升级烙痕"):
            self.laohen_up()
        if self.config.get("领任务奖励"):
            self.claim_quest()
            self.claim_dayueka()
            self.claim_guild()
        self.log_info("收菜完成!", True)

    def claim_guild(self):
        self.click_relative(0.19, 0.06)
        self.click_to_continue_wait(time_out=3)
        self.click_relative(0.5, 0.06)
        self.sleep(1)
        self.click_relative(0.56, 0.37)
        self.wait_click_ocr(0.70, 0.28, 0.81, 0.36, match="领取奖励", time_out=3)
        self.sleep(1)
        self.click_to_continue_wait(time_out=3)
        self.sleep(1)
        self.click_relative(0.56, 0.06)
        self.sleep(1)
        self.go_home_wait()

    def claim_dayueka(self):
        self.choose_main_menu("活动中心")
        if self.wait_click_ocr(0.02, 0.09, 0.16, 0.91, match='叶脉联结'):
            if self.wait_click_ocr(0.35, 0.80, 0.44, 0.85, match="任务总览", time_out=4):
                if self.wait_click_ocr(0.68, 0.80, 0.77, 0.85, match="全部领取", time_out=3):
                    self.wait_until(lambda: self.ocr(0.35, 0.80, 0.44, 0.85, match="任务总览"),
                                    post_action=lambda: self.click_relative(0.5, 0.9))
                self.wait_click_ocr(0.2, 0.4, 0.27, 0.44, match="本周任务")
                if self.wait_click_ocr(0.68, 0.80, 0.77, 0.85, match="全部领取", time_out=3):
                    self.wait_until(lambda: self.ocr(0.35, 0.80, 0.44, 0.85, match="任务总览"),
                                    post_action=lambda: self.click_relative(0.5, 0.9))
        self.go_home_wait()

    def claim_quest(self):
        self.wait_click_ocr(box=self.main_menu_zone, match=re.compile(r"任务"))
        self.wait_click_ocr(0.03, 0.2, 0.16, 0.83, match="日常")
        if self.wait_click_ocr(0.8, 0.75, 0.93, 0.81, match=re.compile(r"领取"), time_out=4):
            self.click_to_continue_wait(time_out=6)
        self.wait_click_ocr(0.03, 0.2, 0.16, 0.83, match="周常")
        if self.wait_click_ocr(0.8, 0.75, 0.93, 0.81, match=re.compile(r"领取"), time_out=4):
            self.click_to_continue_wait(time_out=6)
        self.wait_until(self.check_is_main, post_action=lambda: self.click_relative(0.37, 0.05), time_out=10)

    def laohen_up(self):
        self.choose_main_menu("记忆烙痕")
        self.wait_click_ocr(.86, 0.02, 0.95, 0.07, match="排序与筛选")
        boxes = self.wait_ocr(0.3, 0.3, 0.73, 0.77, match=["等级", "特质等级", "确认设置"])
        self.click_box(boxes[1])
        self.sleep(0.5)
        self.click_box(boxes[0])
        self.sleep(0.5)
        self.click_box(boxes[0])
        self.sleep(0.5)
        self.click_box(boxes[2])
        self.sleep(1)
        self.click_relative(0.71, 0.35)
        self.wait_click_ocr(0.72, 0.85, 0.89)
        self.sleep(1)
        self.click_relative(0.74, 0.62)
        self.sleep(1)
        self.click_relative(0.62, 0.79)
        self.sleep(3)
        self.click_relative(0.5, 0.95)
        self.sleep(3)
        self.click_relative(0.5, 0.95)
        self.go_home_wait()

    def hecha(self):
        self.go_into_menu("午后茶憩", confirm=True)
        for i in range(3):
            self.wait_ocr(0.84, 0.56, 0.95, 0.70, match="台球", time_out=30)
            self.click_relative(0.9, 0.84)
            moqi = self.wait_ocr(0.46, 0.26, 0.54, 0.31, match="默契值", time_out=4)
            if moqi:
                if i == 0:
                    self.click_box(moqi)
                    self.sleep(1)
                    self.click_box(moqi)
                    self.sleep(1)
                self.click_relative(0.4, 0.4)
                self.sleep(1)
                self.click_relative(0.82, 0.78)

            self.heyici()
        self.go_back_confirm()

    def heyici(self):
        diandan = self.wait_until(
            condition=lambda: self.ocr(0.8, 0.83, 0.95, 0.95, match="再来一杯") or
                              self.ocr(0.8, 0.7, 0.95, 0.83, match="开始点单") or
                              self.find_feature("hecha_chat",
                                                x=0.65, y=0.31,
                                                to_x=0.93,
                                                to_y=0.77,
                                                threshold=0.8),
            post_action=lambda: self.click_relative(0.5, 0.95), time_out=60)
        if not diandan:
            self.log_error("找不到开始点单")
            raise Exception("找不到开始点单")

        if diandan[0].name == '再来一杯':  # 如果是喝完直接跳过
            self.click_box(diandan)
        elif diandan[0].name == '开始点单':  # 如果是喝完直接跳过
            self.click_box(diandan)
            while True:
                next_step = self.wait_ocr(.76, .74, .9, .85, match=["下一步", "开始制作"], time_out=3)
                if not next_step:
                    break
                boxes = self.ocr(0.64, 0.23, .9, .74)
                for box in boxes:
                    self.click_box(box)
                    self.sleep(0.2)
                self.click_box(next_step)
        self.wait_until(self.check_hewan, time_out=120)

    def check_hewan(self):
        end = self.ocr(.86, .7, .95, .81, match="结束茶憩")
        choices = self.find_feature("hecha_chat", x=0.65, y=0.31, to_x=0.93, to_y=0.77, threshold=0.8)
        if end:
            self.click_box(end)
            self.sleep(2)
            self.click_relative(.96, 0.5)
            return True
        elif choices:
            choice = random.choice(choices)
            self.click_box(choice)
        else:
            self.click_relative(0.91, 0.91)

    def combat(self):
        self.choose_main_menu("外勤作战")
        # self.wait_click_ocr(.07, .9, .82, match="物资筹备")
        combats = self.find_combats()

        if self.config.get('随机刷材料次数') > 0:
            self.click_box(combats[0])
            self.dingxiang_combat()
        if self.config.get('随机刷技能书次数') > 0:
            combats = self.find_combats()
            self.click_box(combats[1])
            self.guangke_combat()
        self.sleep(1)
        self.go_home_wait()

    def find_combats(self):
        return self.wait_ocr(x=0.07, y=0.8, to_x=0.96, to_y=0.94, match=["定向物资保障", "光刻协议"])

    def guangke_combat(self):
        target_list = self.wait_ocr(x=0.03, y=0.36, to_y=0.63, match=re.compile(r"协议"))

        self.click_box(random.choice(target_list))
        self.fast_combat(self.config.get("随机刷技能书次数"))

    def dingxiang_combat(self):
        sub_list = self.wait_until(lambda: self.ocr(x=0.1, y=0.25, to_x=0.9, to_y=0.4, match="百炼成钢"))
        sub_list.append(self.ocr(x=0.1, y=0.25, to_x=0.9, to_y=0.4, match="森严壁垒"))
        main_list = self.ocr(x=0.6, y=0.25, to_x=0.9, to_y=0.8, match=["人造机械", "矿石材料", "结晶宝石"])

        self.click_box(random.choice(main_list))
        self.sleep(0.2)
        self.click_box(random.choice(sub_list))
        self.fast_combat(self.config.get("随机刷材料次数"))
        self.wait_click_ocr(to_x=0.2, to_y=0.1, match="返回")
        self.sleep(2)

    def fast_combat(self, target_count):
        while True:
            self.wait_click_ocr(0.7, 0.8, to_x=0.9, match="快速战斗")
            yao = self.wait_ocr(0.2, 0.5, 0.8, 0.8, match=re.compile(r"^可回复行动力"), time_out=4)
            if yao:
                self.eat_yao(yao)
            else:
                break
        count = 1
        while count < target_count:
            boxes = self.wait_ocr(0.5, 0.2, 0.7, 0.45, match=["补充", "+"])
            plus = self.box_of_screen(923 / 1600, 325 / 900, 977 / 1600, 358 / 900)
            add_stam = boxes[0]
            black_percent = calculate_color_percentage(self.frame, plus_button_black_color, plus)
            self.log_debug(f'检查体力药加号 black_percent: {black_percent} {count}')
            if black_percent > 0.1:
                self.click_box(plus)
                self.sleep(1)
                count += 1
            else:  # 需要吃药
                self.log_info(f"吃体力药 {count}")
                self.click_box(add_stam)
                yao = self.wait_ocr(0.2, 0.5, 0.8, 0.8, match=re.compile(r"^可回复行动力"), time_out=4)
                if not yao:
                    raise ValueError("找不到体力药")
                self.eat_yao(yao)

        self.wait_click_ocr(0.5, 0.7, to_x=0.7, to_y=0.9, match="快速战斗")
        self.sleep(3)
        self.click_relative(0.9, 0.5)
        self.sleep(1)
        self.click_relative(0.9, 0.5)

    def eat_yao(self, yao):
        self.info["使用体力药"] = self.info.get("使用体力药", 0) + 1
        if self.info["使用体力药"] > 10:
            raise Exception("吃了太多体力药!脚本可能出错")
        self.click_box(yao)
        self.wait_confirm()
        self.sleep(1)
        self.click_relative(0.9, 0.5)
        self.sleep(1)

    # def wait_combat
    #     complete = self.ocr

    def friends(self):
        self.sleep(2)
        self.click_relative(225 / 1600, 43 / 900)
        self.wait_click_ocr(0.08, 0.10, 0.20, 0.21, match="好友列表")
        self.wait_click_ocr(0.8, to_y=0.15, match=re.compile(".*赠送$"))
        self.click_to_continue_wait(time_out=3)
        self.go_home_wait()

    def go_shopping(self):
        self.choose_main_menu("有猫零售")
        self.wait_click_box(lambda: self.ocr(box=self.box_of_screen(0, 0.1, to_x=0.3), match="精选礼包"))
        self.sleep(1)
        free = self.ocr(box=self.box_of_screen(0.1, 0.5, to_x=0.5), match="免费")
        if free:
            self.click_box(free)
            self.log_info("点击购买免费礼包")
            self.wait_click_box(lambda: self.ocr(box=self.box_of_screen(0.5, 0.5, to_x=0.8), match=re.compile("购")))
            self.click_to_continue_wait()
        else:
            self.log_info("已经买过免费礼包")
        self.go_home_wait()

    def click_last_summon(self):
        laohens = self.ocr(box=self.box_of_screen(0, 0.47, to_x=0.3), match="记忆烙痕")
        if len(laohens) > 0:
            self.click_box(laohens[-1])
            return True

    def free_summon(self):
        self.choose_main_menu("精神深潜")
        self.wait_until(self.click_last_summon)
        if self.wait_click_ocr(0.5, 0.8, match="无消耗", time_out=4):
            self.log_info("开始免费召唤")
            self.wait_click_ocr(0.9, 0, to_y=0.2, match="SKIP")
            self.wait_click_ocr(0.4, 0.8, to_x=0.6, match=re.compile(r"^确"))
            self.click_to_continue_wait()
        else:
            self.log_info("免费召唤次数没了")
        self.go_home_wait()

    def shoucai(self):
        self.go_into_menu("白荆穹顶", True)
        self.wait_click_ocr(0.9, 0.9, match="全部收取", time_out=40)
        self.click_to_continue_wait()
        self.go_back_confirm()

    def go_back_confirm(self):
        self.wait_click_ocr(to_x=0.2, to_y=0.1, match="返回")
        self.wait_confirm()
        self.wait_main()


plus_button_black_color = {
    'r': (40, 70),  # Red range
    'g': (40, 70),  # Green range
    'b': (40, 70)  # Blue range
}

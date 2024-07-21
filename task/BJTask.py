import re

from ok.color.Color import white_color
from ok.feature.Box import find_box_by_name
from ok.feature.FindFeature import FindFeature
from ok.ocr.OCR import OCR
from ok.task.BaseTask import BaseTask


class BJTask(BaseTask, OCR, FindFeature):
    def __init__(self):
        super(BJTask, self).__init__()
        self.main_menu_buttons = None
        self.menu_name_list = ['外勤作战', '回廊漫巡']
        self.auto_combat_timeout = 600

    def ensure_main_page(self):
        if self.go_home_now():
            return True
        result = self.wait_until(self.check_until_main, time_out=120)
        if not result:
            self.log_error('无法进入到主页，请手动进入游戏主页！', notify=True)
            return False
        elif isinstance(result, str):
            self.log_error(result, notify=True)
            return False
        else:
            self.log_info("进入主页成功", notify=True)
            return True

    def click_to_continue_wait(self, time_out=0):
        while self.wait_click_ocr(0.42, 0.74, 0.58, 0.97, match=re.compile(r"^点击"), time_out=time_out):
            pass

    def click_to_continue(self):
        click_to_continue = self.ocr(0.42, 0.74, 0.58, 0.97, match=re.compile(r"^点击"))
        if click_to_continue:
            self.click_box(click_to_continue)
            return True

    def go_home_wait(self):

        self.wait_click_feature('go_home')
        return self.wait_main()

    def wait_main(self):
        return self.wait_until(self.find_world)

    def go_home_now(self):
        go_home = self.find_feature('go_home', threshold=0.92)
        if go_home:
            self.log_info("返回主页")
            self.click_box(go_home)
            self.sleep(4)
            return True

    def choose_main_menu(self, name):
        self.go_into_menu(name)

    def check_until_main(self):
        self.info['检查主页次数'] = self.info.get("检查主页次数", 1) + 1
        self.log_debug(f'check check_until_main {self.info.get("检查主页次数")}')
        main = self.ocr(.91, 0.91, 0.96, 0.96, match="功能菜单")
        self.log_debug(f'found main menu {main}')
        if main:
            while True:
                task = self.find_world()
                if task:
                    break
                if self.click_to_continue():
                    continue
                qiandao_lingqu = self.ocr(0.2, 0.6, 0.8, match="可领取")
                if qiandao_lingqu:
                    self.click_box(qiandao_lingqu)
                    self.sleep(2)
                    self.click_relative(0.4, 0.05)
                    self.sleep(2)
                    continue
                else:
                    self.log_debug(f'found main_screen_feature {main}')
                    self.click_relative(0.4, 0.05)
                    self.sleep(2)
                self.click_to_continue()
            self.sleep(3)  # wait for animation
            if self.find_world():
                return True
        start = self.find_one('start_screen_feature',
                              threshold=0.9, use_gray_scale=True)
        self.log_debug(f'found start feature {start}')
        if start:
            boxes = self.ocr(0.5, 0.5)
            if find_box_by_name(boxes, "微信登录"):
                self.log_info('需要登陆账号', notify=True)
                self.disable()
                return "需要登陆账号"
            if box := find_box_by_name(boxes, "点击进入游戏"):
                self.click_box(box)
                return False

            self.log_debug(f'found start_screen_feature {start}')
            self.click_relative(0.88, 0.5)
            self.sleep(2)
            return False
        self.click_to_continue()

    def find_world(self):
        world = self.ocr(box=self.main_menu_zone, match=re.compile(r"世界"), log=True)
        if world:
            white_color_percent = self.calculate_color_percentage(white_color, world[0])
            self.log_debug(f'world white percent {white_color_percent}')
            return white_color_percent > 0.05

    def go_into_menu(self, menu, confirm=False):
        self.wait_click_ocr(0.9, 0.9, match="功能菜单")
        self.wait_click_ocr(0.6, 0.1, to_y=0.8, match=menu)
        if confirm:
            self.wait_confirm()

    def wait_confirm(self):
        self.wait_click_ocr(0.5, 0.5, to_x=0.8, to_y=0.8, match=re.compile('^确'))

    @property
    def star_combat_zone(self):
        return self.box_of_screen(0.8, 0.8, width=0.2, height=0.2, name="star_combat_zone")

    @property
    def main_menu_zone(self):
        return self.box_of_screen(0.62, 0.60, 0.97, 0.87, name="主页菜单区域")
        # return self.box_of_screen(0, 0, 1, 1, name="主页菜单区域")

    def check_is_main(self):
        return self.find_world()

    def main_go_to_manxun(self):
        self.go_into_menu('回廊漫巡')

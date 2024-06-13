import re

from ok.feature.Box import boxes_to_map_by_list_of_names, find_box_by_name
from ok.feature.FindFeature import FindFeature
from ok.ocr.OCR import OCR
from ok.task.OneTimeTask import OneTimeTask


class BJTask(OneTimeTask, OCR, FindFeature):
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
        return self.wait_click_ocr(0.42, 0.74, 0.58, 0.97, match=re.compile(r"^点击"), time_out=time_out)

    def click_to_continue(self):
        click_to_continue = self.ocr(0.42, 0.74, 0.58, 0.97, match=re.compile(r"^点击"))
        if click_to_continue:
            self.click_box(click_to_continue)
            return True

    def go_home_wait(self):
        self.wait_click_feature('go_home')
        return self.wait_main()

    def wait_main(self):
        return self.wait_until(lambda: self.ocr(box=self.main_menu_zone, match=re.compile(r"完成")))

    def go_home_now(self):
        go_home = self.find_feature('go_home', threshold=0.92)
        if go_home:
            self.log_info("返回主页")
            self.click_box(go_home)
            self.sleep(4)
            return True

    def choose_main_menu(self, name):
        self.wait_click_box(lambda: self.ocr(box=self.main_menu_zone, match=name), time_out=20)

    def check_until_main(self):
        self.info['检查主页次数'] = self.info.get("检查主页次数", 1) + 1
        self.log_debug(f'check check_until_main {self.info.get("检查主页次数")}')
        main = self.find_one('main_screen_feature', threshold=0.9, use_gray_scale=True)
        self.log_debug(f'found main menu {main}')
        if main:
            while True:
                task = self.ocr(box=self.main_menu_zone, match="外勤作战")
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
            if self.ocr(box=self.main_menu_zone, match=re.compile(r"外勤作战")):
                return True
        start = self.find_one('start_screen_feature',
                              threshold=0.9, use_gray_scale=True)
        self.log_debug(f'found start feature {start}')
        if start:
            boxes = self.ocr(box=self.box_of_screen(0.5, 0.5))
            if find_box_by_name(boxes, "微信登陆"):
                return "需要登陆账号"
            self.log_debug(f'found start_screen_feature {start}')
            self.click_relative(0.88, 0.5)
            self.sleep(2)
            return False
        self.click_to_continue()

    def go_into_menu(self, menu, confirm=False):
        self.wait_click_ocr(0.9, 0.9, match="菜单")
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
        return self.box_of_screen(0.62, 0.31, 0.97, 0.65, name="主页菜单区域")

    def check_is_main(self):
        boxes = self.ocr(box=self.main_menu_zone)
        self.main_menu_buttons = boxes_to_map_by_list_of_names(boxes, self.menu_name_list)
        if self.main_menu_buttons:
            return True

    def main_go_to_manxun(self):
        self.click_box(self.main_menu_buttons['回廊漫巡'])

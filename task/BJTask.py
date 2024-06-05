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

    def check_until_main(self):
        self.info['检查主页次数'] = self.info.get("检查主页次数", 1) + 1
        self.log_debug(f'check check_until_main {self.info.get("检查主页次数")}')
        main = self.find_one('main_screen_menu', threshold=0.4)
        self.screenshot("main_screen_menu.png")
        if main:
            self.log_debug(f'found main menu {main}')
            click_to_continue = self.find_one('click_to_continue')
            if click_to_continue:
                self.click_box(click_to_continue)
                self.sleep(2)
                return False
            qiandao_lingqu = self.ocr(self.get_box_by_name('box_qiandao'), match="可领取")
            if qiandao_lingqu:
                self.click_box(qiandao_lingqu)
                self.sleep(2)
                self.click_relative(0.4, 0.05)
                self.sleep(2)
                return False
            task = self.ocr(self.box_of_screen(0.6, 0.3, to_y=0.9), match="任务")
            if task:
                self.sleep(3)  # wait for animation
                task = self.ocr(self.box_of_screen(0.6, 0.3, to_y=0.9), match="任务")
            if task:
                return True
            else:
                self.log_debug(f'found main_screen_feature {main}')
                self.click_relative(0.4, 0.05)
                self.sleep(2)
                return True
        start = self.find_one('start_screen_feature')
        if start:
            boxes = self.ocr(self.box_of_screen(0.5, 0.5))
            if find_box_by_name(boxes, "微信登陆"):
                return "需要登陆账号"
            self.log_debug(f'found start_screen_feature {start}')
            self.click_relative(0.88, 0.5)
            self.sleep(2)

    @property
    def star_combat_zone(self):
        return self.box_of_screen(0.8, 0.8, 0.2, 0.2, name="star_combat_zone")

    @property
    def main_menu_zone(self):
        return self.box_of_screen(0.5, 0.4, 0.5, 0.5)

    def check_is_main(self):
        boxes = self.ocr(self.main_menu_zone)
        self.main_menu_buttons = boxes_to_map_by_list_of_names(boxes, self.menu_name_list)
        if self.main_menu_buttons:
            return True

    def main_go_to_manxun(self):
        self.click_box(self.main_menu_buttons['回廊漫巡'])

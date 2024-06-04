from ok.feature.Box import boxes_to_map_by_list_of_names
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
        if not self.wait_until(self.check_until_main, time_out=60):
            self.log_error('无法进入到主页，请手动进入游戏主页！', notify=True)
            return False
        else:
            self.log_info("进入主页成功", notify=True)
            return True

    def check_until_main(self):
        self.info['检查主页次数'] = self.info.get("检查主页次数", 1) + 1
        main = self.find_one('main_screen_feature', horizontal_variance=0.02, vertical_variance=0.02)
        if main:
            self.log_debug(f'found main_screen_feature {main}')
            self.click_relative(0.4, 0.05)
            self.sleep(2)
            return True
        start = self.find_one('start_screen_feature', horizontal_variance=0.02, vertical_variance=0.02)
        if start:
            self.log_debug(self, f'found start_screen_feature {start}')
            self.click_relative(0.95, 0.5)
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

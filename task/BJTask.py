from ok.feature.Box import boxes_to_map_by_list_of_names
from ok.ocr.OCR import OCR
from ok.task.OneTimeTask import OneTimeTask


class BJTask(OneTimeTask, OCR):
    def __init__(self):
        super(BJTask, self).__init__()
        self.main_menu_buttons = None
        self.menu_name_list = ['外勤作战', '回廊漫巡']
        self.auto_combat_timeout = 600

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

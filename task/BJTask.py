from ok.ocr.OCR import OCR
from ok.task.BaseTask import BaseTask


class BJTask(BaseTask, OCR):
    def __init__(self):
        super(BJTask, self).__init__()
        self.auto_combat_timeout = 600

    @property
    def star_combat_zone(self):
        return self.box_of_screen(0.8, 0.8, 0.2, 0.2)

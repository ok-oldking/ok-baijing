from typing_extensions import override

from autohelper.feature.Box import find_box_by_name
from autohelper.logging.Logger import get_logger
from autohelper.ocr.OCR import OCR
from autohelper.task.BaseTask import BaseTask

logger = get_logger(__name__)


class ManXunTask(BaseTask, OCR):
    def __init__(self):
        super().__init__()
        self.confirm_box = None
        self.down_choice = None
        self.upper_choice = None
        self.middle_choice = None
        self.click_no_brainer = ["直接胜利", "漫巡推进"]

    @override
    def run_frame(self):
        boxes = self.ocr()
        self.down_choice = find_box_by_name(boxes, "漫巡推进")
        if self.down_choice is None:
            logger.error("必须从有漫巡推进的按钮处开始")
            self.set_done()
            return False
        self.middle_choice = self.down_choice.copy(y_offset=self.down_choice.height * 3)
        self.upper_choice = self.middle_choice.copy(y_offset=self.down_choice.height * 3)
        self.next_frame()
        self.click_box(self.down_choice)
        self.sleep(1)
        boxes = self.ocr()
        self.confirm_box = find_box_by_name(boxes, "前进")
        self.click_box(self.confirm_box)
        self.sleep(1)
        self.logger.info("初始化完成")

        self.set_done()

    def loop(self):
        while True:
            self.click_box(self.down_choice)
            self.sleep(1)
            boxes = self.ocr()

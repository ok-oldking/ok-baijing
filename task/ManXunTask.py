import time

from typing_extensions import override

from autohelper.logging.Logger import get_logger
from autohelper.ocr.OCR import OCR
from autohelper.task.BaseTask import BaseTask

logger = get_logger(__name__)


class ManXunTask(BaseTask, OCR):

    @override
    def run_frame(self):
        logger.debug('ManXunTask.run_frame ocr')
        start = time.time()
        boxes = self.ocr()
        logger.debug(f'ManXunTask.run_frame ocr {len(boxes)} boxes {time.time() - start}')
        self.sleep(1)

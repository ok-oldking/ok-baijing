import time

from autohelper.feature.Box import Box, sort_boxes, find_boxes_by_name
from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class OCR:

    def __init__(self):
        self.executor = None
        self.default_threshold = 0.9

    def ocr(self, box: Box = None, match=None, threshold=0):
        if threshold == 0:
            threshold = 0.9
        start = time.time()
        image = self.frame
        if image is not None:
            if box is not None:
                x, y, w, h = box.x, box.y, box.width, box.height
                image = image[y:y + h, x:x + w]

            result = self.executor.ocr.ocr(image)

            detected_boxes = []
            # Process the results and create Box objects
            for res in result:
                if res is not None:
                    for line in res:
                        pos = line[0]
                        text, confidence = line[1]
                        if confidence >= threshold:
                            detected_box = Box(int(pos[0][0]), int(pos[0][1]), int(pos[2][0] - pos[0][0]),
                                               int(pos[2][1] - pos[0][1]),
                                               confidence, text)
                            if box is not None:
                                detected_box.x += box.x
                                detected_box.y += box.y
                            detected_boxes.append(detected_box)
            if match is not None:
                detected_boxes = find_boxes_by_name(detected_boxes, match)
            communicate.draw_box.emit("ocr", detected_boxes, "red")
            communicate.draw_box.emit("ocr_zone", box, "blue")
            logger.debug(f"ocr_zone {box} found result: {len(detected_boxes)}) time: {time.time() - start}")
            return sort_boxes(detected_boxes)

    def find_text(self, text, box: Box = None, confidence=0):
        for result in self.ocr(box, confidence):
            if result.name == text:
                return result

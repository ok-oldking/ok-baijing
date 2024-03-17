from typing import List

from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate


class OCR:

    def __init__(self):
        self.executor = None
        self.default_threshold = 0.9

    def ocr(self, box: Box = None, threshold=0) -> List[Box]:
        if threshold == 0:
            threshold = 0.9
        image = self.frame
        if image is not None:
            if box is not None:
                x, y, w, h = box.x, box.y, box.width, box.height
                image = image[y:y + h, x:x + w]

            # Convert the ROI to a format PaddleOCR can work with
            # roi_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Initialize the OCR model

            # Perform OCR on the extracted ROI
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
                            detected_boxes.append(detected_box)
            communicate.draw_box.emit("", detected_boxes)
            return detected_boxes

    def find_text(self, text, box: Box = None, confidence=0):
        for result in self.ocr(box, confidence):
            if result.name == text:
                return result

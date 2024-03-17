from typing import List

from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate


class OCR:

    def __init__(self):
        self.executor = None

    def ocr(self, box: Box = None) -> List[Box]:
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
            result = self.executor.ocr(image)

            detected_boxes = []
            # Process the results and create Box objects
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    pos = line[0]
                    text, confidence = line[1]
                    detected_box = Box(int(pos[0][0]), int(pos[0][1]), int(pos[2][0] - pos[0][0]),
                                       int(pos[2][1] - pos[0][1]),
                                       confidence, text)
                    detected_boxes.append(detected_box)
                    print(detected_box)
            communicate.draw_box.emit("", detected_boxes)
            return detected_boxes

    @staticmethod
    def draw_boxes(boxes, feature_name):
        communicate.draw_box.emit(feature_name, boxes)

    def on_feature(self, boxes):
        pass

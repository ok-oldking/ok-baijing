import time
from typing import List

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QImage, QPixmap, QColor, QPen, QFont
from PySide6.QtWidgets import QWidget

from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate


class FrameWidget(QWidget):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.cv_image = None
        self.brush_color = QColor(255, 0, 0)
        self.uiDict = {}
        self.time_to_expire = 3
        communicate.frame.connect(self.set_image)
        communicate.draw_box.connect(self.draw_box)

    def remove_expired(self):
        current_time = time.time()
        for key in list(self.uiDict.keys()):
            # Filter out the old UI elements and keep the remaining ones
            if current_time - self.uiDict[key][1] > self.time_to_expire:
                del self.uiDict[key]

    def draw_box(self, key: str, boxes: List[Box]):
        if key == "click":
            self.uiDict.clear()
        self.uiDict[key] = [boxes, time.time()]
        self.update()

    def set_image(self, cv_image):
        """Set the OpenCV image to be displayed."""
        self.cv_image = cv_image
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        current = time.time()
        if self.cv_image is not None:
            frame = np.ascontiguousarray(self.cv_image)
            # frame = self.cv_image
            frame_height, frame_width = frame.shape[:2]
            painter = QPainter(self)
            # Convert the OpenCV image (BGR) to QImage format (RGB)
            # h, w, ch = self.cv_image.shape
            # bytes_per_line = ch * w
            # convert_to_Qt_format = QImage(self.cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # qt_image = convert_to_Qt_format.rgbSwapped()

            qt_image = QImage(frame.data, frame.shape[1], frame.shape[0],
                              frame.strides[0],
                              QImage.Format_BGR888)
            # qt_image = QImage(frame.data, frame.shape[1], frame.shape[0],
            #                   frame.strides[0],
            #                   QImage.Format_RGBA8888)

            # Scaling the image to fit the aspect ratio of the widget
            qt_image = qt_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Calculate the position to center the image in the widget
            x_offset = (self.width() - qt_image.width()) / 2
            y_offset = (self.height() - qt_image.height()) / 2

            frame_ratio = qt_image.width() / frame_width

            painter.drawPixmap(x_offset, y_offset, QPixmap.fromImage(qt_image))
            pen = QPen(self.brush_color)  # Set the brush to red color
            pen.setWidth(2)  # Set the width of the pen (border thickness)
            painter.setPen(pen)  # Apply the pen to the painter
            painter.setBrush(Qt.NoBrush)  # Ensure no fill
            painter.setFont(QFont('Arial', 12))
            # Draw a square. Arguments are (x, y, width, height).
            # Adjust these values according to the desired size and position.
            self.remove_expired()
            for key, value in self.uiDict.items():
                boxes = value[0]
                for box in boxes:
                    width = box.width * frame_ratio
                    height = box.height * frame_ratio
                    x = x_offset + box.x * frame_ratio
                    y = y_offset + box.y * frame_ratio
                    painter.drawRect(x, y, width, height)
                    # Draw text at the specified position
                    painter.drawText(x, y + height + 12, f"{key}_{round(box.confidence * 100)}")
        # print(f"draw rect: {time.time() - current}")

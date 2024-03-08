from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QImage, QPixmap
from PySide6.QtWidgets import QWidget

from autoui.gui.Communicate import communicate


class FrameWidget(QWidget):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.aspect_ratio = 16 / 9
        self.cv_image = None
        communicate.frame.connect(self.set_image)

    def set_image(self, cv_image):
        """Set the OpenCV image to be displayed."""
        self.cv_image = cv_image
        self.aspect_ratio = self.cv_image.shape[1] / self.cv_image.shape[0]
        # self.parent.set_ratio(ratio)
        # print(f"aspect_ratio: {self.aspect_ratio}")
        self.update()  # Trigger a repaint

    # def resizeEvent(self, event):
    #     w = event.size().width()
    #     h = event.size().height()
    #     new_ratio = w / h
    #     new_width = h * self.aspect_ratio
    #     new_height = w / self.aspect_ratio
    #     if new_ratio > self.aspect_ratio:
    #         print("new 1")
    #         self.setFixedSize(QSize(w, new_height))
    #     else:
    #         print("new 2")
    #         self.setFixedSize(QSize(new_width, h))
    #     super().resizeEvent(event)

    def paintEvent(self, event):
        if self.cv_image is not None:
            painter = QPainter(self)
            # Convert the OpenCV image (BGR) to QImage format (RGB)
            # h, w, ch = self.cv_image.shape
            # bytes_per_line = ch * w
            # convert_to_Qt_format = QImage(self.cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # qt_image = convert_to_Qt_format.rgbSwapped()

            qt_image = QImage(self.cv_image.data, self.cv_image.shape[1], self.cv_image.shape[0],
                              self.cv_image.strides[0],
                              QImage.Format_BGR888)

            # Scaling the image to fit the aspect ratio of the widget
            qt_image = qt_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Calculate the position to center the image in the widget
            x = (self.width() - qt_image.width()) / 2
            y = (self.height() - qt_image.height()) / 2
            painter.drawPixmap(x, y, QPixmap.fromImage(qt_image))

import cv2
import numpy as np

from ok.save.PostProcessor import PostProcessor


class BlackBarProcessor(PostProcessor):
    def __init__(self, x, y, width, height, color=(1, 1, 1)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def process(self, image: np.ndarray):
        height, width = image.shape[:2]
        # Calculate absolute coordinates
        x = int(self.x * width)
        y = int(self.y * height)
        abs_width = int(self.width * width)
        abs_height = int(self.height * height)

        # Draw a black rectangle
        cv2.rectangle(image, (x, y), (x + abs_width, y + abs_height), self.color, -1)
        print(f"cv2.rectangle ({x},{y},{abs_width},{abs_height})")

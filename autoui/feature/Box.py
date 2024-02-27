import random


class Box:
    def __init__(self, x: int, y: int, width: int, height: int, confidence: float = 1, name=None) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence

    def __str__(self) -> str:
        if self.name is not None:
            return f"Box(name='{self.name}', x={self.x}, y={self.y}, width={self.width}, height={self.height}, confidence={self.confidence})"
        return f"Box(x={self.x}, y={self.y}, width={self.width}, height={self.height}, confidence={self.confidence})"

    def relative_with_variance(self, relative_x=0.5, relative_y=0.5):
        # Calculate the center of the box
        center_x = self.x + self.width * relative_x
        center_y = self.y + self.height * relative_y

        # Add random variance
        variance = random.uniform(0, 0.1)
        center_x_with_variance = center_x + variance
        center_y_with_variance = center_y + variance
        return round(center_x_with_variance), round(center_y_with_variance)


def sort_boxes(boxes):
    return sorted(boxes, key=lambda box: (box.y, box.x if abs(box.y - boxes[0].y) < 6 else 0))

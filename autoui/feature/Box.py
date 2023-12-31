import random


class Box:
    def __init__(self, x: int, y: int, width: int, height: int, confidence: float = 1) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence

    def __str__(self) -> str:
        return f"Box(x={self.x}, y={self.y}, width={self.width}, height={self.height}, confidence={self.confidence})"

    def center_with_variance(self):
        # Calculate the center of the box
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        # Add random variance
        variance = random.uniform(0, 0.1)
        center_x_with_variance = center_x + variance
        center_y_with_variance = center_y + variance
        return round(center_x_with_variance), round(center_y_with_variance)

    def sort_boxes(boxes):
        return sorted(boxes, key=lambda box: (box.y, box.x if abs(box.y - boxes[0].y) < 6 else 0))

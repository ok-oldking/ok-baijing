import random


class Box:
    def __init__(self, x: int, y: int, width: int, height: int, confidence: float = 1, name=None) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence

    def __eq__(self, other):
        if not isinstance(other, Box):
            # Don't attempt to compare against unrelated types
            return NotImplemented

        return (self.x == other.x and
                self.y == other.y and
                self.width == other.width and
                self.height == other.height and
                self.confidence == other.confidence and
                self.name == other.name)

    def __str__(self) -> str:
        if self.name is not None:
            return f"Box(name='{self.name}', x={self.x}, y={self.y}, width={self.width}, height={self.height}, confidence={round(self.confidence * 100)})"
        return f"Box(x={self.x}, y={self.y}, width={self.width}, height={self.height}, confidence={round(self.confidence * 100)})"

    def relative_with_variance(self, relative_x=0.5, relative_y=0.5):
        # Calculate the center of the box
        center_x = self.x + self.width * relative_x
        center_y = self.y + self.height * relative_y

        # Add random variance
        variance = random.uniform(0, 0.1)
        center_x_with_variance = center_x + variance
        center_y_with_variance = center_y + variance
        return round(center_x_with_variance), round(center_y_with_variance)

    def copy(self, x_offset=0, y_offset=0, name=None):
        return Box(self.x + x_offset, self.y + y_offset, self.width, self.height, self.confidence, name or self.name)


def sort_boxes(boxes):
    return sorted(boxes, key=lambda box: (box.y, box.x if abs(box.y - boxes[0].y) < 6 else 0))


def find_box_by_name(boxes, names):
    names = [names] if isinstance(names, str) else names

    result = None
    priority = len(names)

    for box in boxes:
        if box.name in names:
            index = names.index(box.name)
            if index < priority:
                priority = index
                result = box
                if priority == 0:
                    break

    if result is not None:
        return result

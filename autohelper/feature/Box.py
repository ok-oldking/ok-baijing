import math
import random
import re


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

    def __repr__(self):
        return self.name

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

    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def find_closest_box(self, direction: str, boxes: list):
        orig_center_x, orig_center_y = self.center()

        def distance_criteria(box):
            # Calculate center points for comparison
            box_center_x, box_center_y = box.center()

            dx = box_center_x - orig_center_x
            dy = box_center_y - orig_center_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if direction == 'up' and dy < 0:
                return distance
            elif direction == 'down' and dy > 0:
                return distance
            elif direction == 'left' and dx < 0:
                return distance
            elif direction == 'right' and dx > 0:
                return distance
            else:
                return float('inf')
                # Filter boxes that are in the specified direction and sort by distance

        filtered_boxes = sorted(boxes, key=distance_criteria)

        # Return the first box in the list, which is the closest, if any are found
        for box in filtered_boxes:
            if distance_criteria(box) != float('inf'):
                return box
        return None


def sort_boxes(boxes):
    return sorted(boxes, key=lambda box: (box.y, box.x if abs(box.y - boxes[0].y) < 6 else 0))


def find_box_by_name(boxes, names) -> Box:
    if isinstance(names, (str, re.Pattern)):
        names = [names]

    result = None
    priority = len(names)

    for box in boxes:
        for i, name in enumerate(names):
            if (isinstance(name, str) and name == box.name) or (
                    isinstance(name, re.Pattern) and re.search(name, box.name)):
                if i < priority:
                    priority = i
                    result = box
                    if i == 0:
                        break

    return result


def find_boxes_by_name(boxes, names) -> list[Box]:
    # Ensure names is always a list
    if isinstance(names, (str, re.Pattern)):
        names = [names]

    result = []

    for box in boxes:
        # Flag to track if the box has been matched and should be added
        matched = False
        for name in names:
            if matched:
                break  # Stop checking names if we've already matched this box
            if (isinstance(name, str) and name == box.name) or (
                    isinstance(name, re.Pattern) and re.search(name, box.name)):
                matched = True
        if matched:
            result.append(box)

    return result

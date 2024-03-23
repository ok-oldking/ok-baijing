from typing import List

from autohelper.color.Color import calculate_color_percentage
from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate

white_color = {
    'r': (220, 255),  # Red range
    'g': (220, 255),  # Green range
    'b': (220, 255)  # Blue range
}

dark_gray_color = {
    'r': (40, 60),  # Red range
    'g': (40, 75),  # Green range
    'b': (40, 85)  # Blue range
}


def find_choice(frame, box, horizontal=0, vertical=0, threshold=0.6) -> Box | None:
    result = find_choices(frame, box, horizontal, vertical, 1, threshold)
    if len(result) > 0:
        return result[0]
    else:
        return None


def find_choices(frame, box, horizontal=0, vertical=0, limit=1000, threshold=0.6) -> List[Box]:
    result = []
    to_find = box
    count = 0
    horizontal = int(horizontal)
    vertical = int(vertical)
    while True:
        to_find = Box(to_find.x + horizontal, to_find.y + vertical, to_find.width, to_find.height)
        percentage_white = calculate_color_percentage(frame, white_color, to_find)
        percentage_grey = calculate_color_percentage(frame, dark_gray_color, to_find)
        to_find.confidence = percentage_grey + percentage_white * 2
        if percentage_white < 0.03:
            to_find.confidence = 0
        if percentage_grey < 0.03:
            to_find.confidence = 0
        if to_find.confidence > threshold:
            count = count + 1
            result.append(to_find)
            if count >= limit:
                break
            if horizontal == 0 and vertical == 0:
                break
        else:
            break
    communicate.draw_box.emit("choices", result, "red")
    return result

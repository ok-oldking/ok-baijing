from typing import List

from autoui.feature.Box import Box


class BaseOverlay:

    def __init__(self) -> None:
        pass

    def draw_boxes(self, key: str, boxes: List[Box], outline: str):
        pass


def draw_boxes(obj, key: str, boxes: List[Box], outline: str = "red"):
    if hasattr(obj, "executor") and obj.executor is not None:
        overlay = obj.executor.overlay
    else:
        overlay = obj.overlay
    # print(f"draw boxes {key}: {overlay}")
    if (overlay is not None) and hasattr(overlay, "draw_boxes"):
        overlay.draw_boxes(key, boxes, outline)

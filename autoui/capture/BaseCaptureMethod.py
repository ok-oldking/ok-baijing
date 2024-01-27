from cv2.typing import MatLike


class BaseCaptureMethod:
    name = "None"
    short_description = ""
    description = ""
    last_captured_frame: MatLike
    top_cut = 0
    bottom_cut = 0
    left_cut = 0
    right_cut = 0
    window_change_listeners = []

    def __init__(self):
        # Some capture methods don't need an initialization process
        pass

    def close(self):
        # Some capture methods don't need an initialization process
        pass

    def get_frame(self) -> MatLike | None:
        pass

    def bring_to_front(self) -> bool:
        pass

    def draw_rectangle(self):
        pass

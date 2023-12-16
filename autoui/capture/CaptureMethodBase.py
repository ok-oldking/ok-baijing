from typing import TYPE_CHECKING

from cv2.typing import MatLike

class CaptureMethodBase:
    name = "None"
    short_description = ""
    description = ""
    last_captured_frame:MatLike
    top_cut = 0
    bottom_cut = 0
    left_cut = 0
    right_cut = 0

    def __init__(self):
        # Some capture methods don't need an initialization process
        pass
   
    def close(self):
        # Some capture methods don't need an initialization process
        pass

    # def get_latest_frame(self) -> :  # noqa: PLR6301
        
    #     return None

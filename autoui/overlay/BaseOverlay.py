from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from typing import List
from autoui.feature.Box import Box

class BaseOverlay:

    def __init__(self) -> None:
        pass
    
    def draw_boxes(self, boxes:List[Box], outline:str):
        pass
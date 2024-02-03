from autoui.capture.windows.WindowsGraphicsCaptureMethod import WindowsCaptureMethodGraphics
from autoui.save.BlackBarProcessor import BlackBarProcessor
from autoui.save.SaveByKeyPress import SaveByKeyPress

capture = WindowsCaptureMethodGraphics("Genshin Impact")
# capture = WindowsGraphicsCaptureMethod("MuMu Player 12")
# capture.bottom_cut = 0.025
cover_uid = BlackBarProcessor(0.87, 0.978, 0.12, 0.1)
save = SaveByKeyPress(capture, cover_uid, capture_key=".", stop_key="/")

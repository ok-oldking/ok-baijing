from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.save.SaveByInterval import SaveByInterval
from autoui.save.SaveByKeyPress import SaveByKeyPress
from autoui.save.BlackBarProcessor import BlackBarProcessor

capture = WindowsGraphicsCaptureMethod("Genshin Impact")
# capture = WindowsGraphicsCaptureMethod("MuMu Player 12")
# capture.bottom_cut = 0.025
cover_uid = BlackBarProcessor(0.87,0.978,0.12,0.1)
save = SaveByKeyPress(capture, cover_uid, capture_key=".", stop_key="/")
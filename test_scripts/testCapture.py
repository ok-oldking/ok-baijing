from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.save.SaveByInterval import SaveByInterval
from autoui.save.SaveByKeyPress import SaveByKeyPress

capture = WindowsGraphicsCaptureMethod("Genshin Impact")
# capture = WindowsGraphicsCaptureMethod("MuMu Player 12")
# capture.bottom_cut = 0.025

save = SaveByKeyPress(capture, capture_key="/")
save.wait_until_done()
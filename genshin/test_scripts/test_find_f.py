from autoui.feature.FeatureSet import FeatureSet
from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.task.FindFeatureAndClickTask import FindFeatureAndClickTask
from autoui.overlay.TkOverlay import TkOverlay
from autoui.overlay.QtOverlay import QtOverlay

# Example usage
capture = WindowsGraphicsCaptureMethod("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

overlay = TkOverlay(capture)

findF = FindFeatureAndClickTask(capture,feature_set,"button_play",horizontal_variance=0.2,vertical_variance=0.2,overlay=overlay)

overlay.start()


from autoui.feature.FeatureSet import FeatureSet
from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.task.FindFeatureAndClickTask import FindFeatureAndClickTask

# Example usage
capture = WindowsGraphicsCaptureMethod("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

findF = FindFeatureAndClickTask(capture,feature_set,"button_f",horizontal_variance=0.2,vertical_variance=0.2)

print("start to find f")
#feature_set.save_images('images')


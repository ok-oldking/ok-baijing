from autoui.feature.FeatureSet import FeatureSet
from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from genshin.task.AutoDialogTask import AutoDialogTask
from autoui.task.TaskExecutor import TaskExecutor
from autoui.overlay.TkWindowed import TkWindow
from autoui.interaction.Win32Interaction import Win32Interaction

# Example usage
capture = WindowsGraphicsCaptureMethod("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

overlay = TkWindow(capture)
interaction = Win32Interaction(capture,overlay)
# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture)
auto_dialog = AutoDialogTask(interaction, feature_set)
task_executor.tasks.append(auto_dialog)

# skip_dialog = SkipDialogTask(interaction,feature_set)
# task_executor.tasks.append(skip_dialog)

overlay.start()


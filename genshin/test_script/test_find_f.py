from autoui.feature.FeatureSet import FeatureSet
from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from genshin.task.AutoPickTask import AutoPickTask
from genshin.task.AutoDialogTask import AutoDialogTask
from autoui.task.TaskExecutor import TaskExecutor
from autoui.overlay.TkOverlay import TkOverlay
from autoui.interaction.Win32Interaction import Win32Interaction

# Example usage
capture = WindowsGraphicsCaptureMethod("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

overlay = TkOverlay(capture)
interaction = Win32Interaction(capture,overlay)
# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture,target_fps=30)
auto_dialog = AutoDialogTask(interaction, feature_set)
task_executor.tasks.append(auto_dialog)

auto_pick = AutoPickTask(interaction, feature_set)
task_executor.tasks.append(auto_pick)

# skip_dialog = SkipDialogTask(interaction,feature_set)
# task_executor.tasks.append(skip_dialog)

overlay.start()


from autoui.overlay.TkWindow import TkWindow

from autoui.capture.windows.WindowsGraphicsCaptureMethod import WindowsCaptureMethodGraphics
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.task.TaskExecutor import TaskExecutor
from genshin.task.AutoPlayDialogTask import AutoDialogTask

# Example usage
capture = WindowsCaptureMethodGraphics("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

overlay = TkWindow(capture)
interaction = Win32Interaction(capture, overlay)
# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture)
auto_dialog = AutoDialogTask(interaction, feature_set)
task_executor.tasks.append(auto_dialog)

# skip_dialog = SkipDialogTask(interaction,feature_set)
# task_executor.tasks.append(skip_dialog)

overlay.start()

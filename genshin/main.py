import threading

from autoui.capture.WindowsGraphicsCaptureMethod import WindowsCaptureMethodGraphics
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.overlay.TkOverlay import TkOverlay
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.DialogScene import DialogScene
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.StartScence import StartScene
from genshin.scene.WorldScene import WorldScene
from genshin.task.AutoDialogTask import AutoDialogTask
from genshin.task.AutoLoginTask import AutoLoginTask
from genshin.task.AutoPickTask import AutoPickTask

exit_event = threading.Event()
# Example usage
capture = WindowsCaptureMethodGraphics("Genshin Impact", exit_event)

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture, target_fps=30, exit_event=exit_event)

overlay = TkOverlay(capture, task_executor.exit_event)
interaction = Win32Interaction(capture, overlay)

task_executor.tasks.append(AutoDialogTask(interaction, feature_set))
task_executor.tasks.append(AutoPickTask(interaction, feature_set))
task_executor.tasks.append(AutoLoginTask(interaction, feature_set))

task_executor.scenes.append(WorldScene(interaction, feature_set))
task_executor.scenes.append(DialogScene(interaction, feature_set))
task_executor.scenes.append(StartScene(interaction, feature_set))
task_executor.scenes.append(MonthlyCardScene(interaction, feature_set))

overlay.start()

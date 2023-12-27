from autoui.capture.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.overlay.TkOverlay import TkOverlay
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.DialogScene import DialogScene
from genshin.scene.WorldScene import WorldScene
from genshin.task.AutoDialogTask import AutoDialogTask
from genshin.task.AutoPickTask import AutoPickTask

# Example usage
capture = WindowsGraphicsCaptureMethod("Genshin Impact")

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture, target_fps=30)

overlay = TkOverlay(capture, task_executor.exit_event)
interaction = Win32Interaction(capture, overlay)

auto_dialog = AutoDialogTask(interaction, feature_set)
task_executor.tasks.append(auto_dialog)

auto_pick = AutoPickTask(interaction, feature_set)
task_executor.tasks.append(auto_pick)

word_scene = WorldScene(feature_set)
task_executor.scenes.append(word_scene)
dialog_scene = DialogScene(feature_set)
task_executor.scenes.append(dialog_scene)

overlay.start()

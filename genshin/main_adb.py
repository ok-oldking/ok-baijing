import threading

import adbutils

from autoui.capture.adb.ADBCaptureMethod import ADBCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.task.TaskExecutor import TaskExecutor
from genshin.scene.BlackDialogScene import BlackDialogScene
from genshin.scene.DialogChoicesScene import DialogChoicesScene
from genshin.scene.DialogCloseButtonScene import DialogCloseButtonScene
from genshin.scene.DialogPlayingScene import DialogPlayingScene
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.StartScence import StartScene
from genshin.scene.WorldScene import WorldScene
from genshin.task.AutoChooseDialogTask import AutoChooseDialogTask
from genshin.task.AutoLoginTask import AutoLoginTask
from genshin.task.AutoPickTask import AutoPickTask
from genshin.task.AutoPlayDialogTask import AutoPlayDialogTask

exit_event = threading.Event()
# Example usage
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

device = adb.device()
capture = ADBCaptureMethod(device)

coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture, target_fps=30, exit_event=exit_event)

# overlay = TkOverlay(capture, task_executor.exit_event)
interaction = Win32Interaction(capture)

task_executor.tasks.append(AutoPlayDialogTask(interaction, feature_set))
task_executor.tasks.append(AutoChooseDialogTask(interaction, feature_set))
task_executor.tasks.append(AutoPickTask(interaction, feature_set))
task_executor.tasks.append(AutoLoginTask(interaction, feature_set))

task_executor.scenes.append(WorldScene(interaction, feature_set))
task_executor.scenes.append(StartScene(interaction, feature_set))
task_executor.scenes.append(MonthlyCardScene(interaction, feature_set))
task_executor.scenes.append(DialogCloseButtonScene(interaction, feature_set))
task_executor.scenes.append(DialogChoicesScene(interaction, feature_set))
task_executor.scenes.append(DialogPlayingScene(interaction, feature_set))
task_executor.scenes.append(BlackDialogScene(interaction, feature_set))

# overlay.start()

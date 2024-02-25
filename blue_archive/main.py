import threading

import adbutils

from autoui.capture.HwndWindow import HwndWindow
from autoui.capture.adb.ADBCaptureMethod import ADBCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.ADBInteraction import ADBBaseInteraction
from autoui.overlay.TkOverlay import TkOverlay
from autoui.task.TaskExecutor import TaskExecutor
from blue_archive.scene.MainScene import MainScene
from blue_archive.scene.NotificationScence import NotificationScene
from blue_archive.scene.StartScence import StartScene
from blue_archive.task.AutoLoginTask import AutoLoginTask
from blue_archive.task.CloseNotificationTask import CloseNotificationTask

exit_event = threading.Event()
# Example usage
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
adb.connect("127.0.0.1:16384")
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

device = adb.device()
capture = ADBCaptureMethod(device)

hwnd_window = HwndWindow(title="Mumu Player 12", exit_event=exit_event, frame_width=capture.width,
                         frame_height=capture.height)

# Setup UI overlay for detection box display, optional
overlay = TkOverlay(hwnd_window, exit_event)
interaction = ADBBaseInteraction(device, capture, overlay)

coco_folder = 'blue_archive/assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height)

# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture, overlay=overlay, interaction=interaction, exit_event=exit_event)

# Defining game scenes to handle different in-game situations through automated tasks
task_executor.scenes.extend([
    StartScene(interaction, feature_set),
    NotificationScene(interaction, feature_set),
    MainScene(interaction, feature_set),
])

# Adding automated tasks for gameplay, such as dialog navigation and item collection
task_executor.tasks.extend([
    AutoLoginTask(interaction, feature_set),
    CloseNotificationTask(interaction, feature_set),
])

overlay.start()

import threading

import adbutils

from autoui.capture.HwndWindow import HwndWindow
from autoui.capture.adb.ADBCaptureMethod import ADBCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.ADBInteraction import ADBBaseInteraction
from autoui.overlay.TkOverlay import TkOverlay
from autoui.task.TaskExecutor import TaskExecutor
from scene.MainScene import MainScene
from scene.NotificationScence import NotificationScene
from scene.OkDialogScene import OkDialogScene
from scene.QuestScene import QuestScene
from scene.StartScence import StartScene
from task.AutoLoginTask import AutoLoginTask
from task.ClickOkTask import ClickOkTask
from task.CloseNotificationTask import CloseNotificationTask
from task.DailyCafeTask import DailyCafeTask
from task.DailyScheduleTask import DailyScheduleTask

exit_event = threading.Event()
# Example usage
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
adb.connect("127.0.0.1:16384")
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

android_package = "com.YostarJP.BlueArchive"
android_activity = "com.yostarjp.bluearchive.MxUnityPlayerActivity"

device = adb.device()
device.shell(f"am start {android_package}/{android_activity}")
capture = ADBCaptureMethod(device)
hwnd_window = HwndWindow(title="Mumu Player 12", exit_event=exit_event, frame_width=capture.width,
                         frame_height=capture.height)

# Setup UI overlay for detection box display, optional
overlay = TkOverlay(hwnd_window, exit_event)
interaction = ADBBaseInteraction(device, capture, overlay)

coco_folder = 'assets/coco_feature'
feature_set = FeatureSet(coco_folder, capture.width, capture.height, overlay=overlay, default_threshold=0.95)

# task_executor = TaskExecutor(capture,target_fps=0.1)
task_executor = TaskExecutor(capture, overlay=overlay, interaction=interaction, exit_event=exit_event, tasks=[
    AutoLoginTask(feature_set),
    CloseNotificationTask(feature_set),
    DailyCafeTask(feature_set),
    DailyScheduleTask(feature_set),
    ClickOkTask(feature_set),
], scenes=[
    OkDialogScene(feature_set),
    StartScene(feature_set),
    NotificationScene(feature_set),
    QuestScene(feature_set),
    MainScene(feature_set),
])

overlay.start()

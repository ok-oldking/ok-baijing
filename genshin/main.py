import threading

from autoui.capture.HwndWindow import HwndWindow
from autoui.capture.windows.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.overlay.TkOverlay import TkOverlay
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

# for graceful shutdown of the script
exit_event = threading.Event()

# Initialize screen capture method with the game window title (supports multilanguage titles)
# Example for English client: capture = WindowsGraphicsCaptureMethod(title="Genshin Impact", exit_event=exit_event)
hwnd_window = HwndWindow(title="原神", exit_event=exit_event)
capture = WindowsGraphicsCaptureMethod(hwnd_window)  # Example for Japanese/Chinese client

# Setup UI overlay for detection box display, optional
overlay = TkOverlay(hwnd_window, exit_event)

# FeatureSet loads in-game UI elements from a COCO-format dataset for accurate automation
coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, hwnd_window.width, hwnd_window.height, overlay=overlay)

interaction = Win32Interaction(capture, overlay)
# TaskExecutor to manage the scenes and tasks
task_executor = TaskExecutor(capture, interaction, overlay=overlay, target_fps=30, exit_event=exit_event, tasks=[
    AutoPlayDialogTask(feature_set),  # speeding up the dialogs
    AutoChooseDialogTask(feature_set),  # choose dialog options
    AutoPickTask(feature_set),  # pickup items in world scene
    AutoLoginTask(feature_set),  # auto login and claim reward
], scenes=[
    WorldScene(feature_set),
    StartScene(feature_set),
    MonthlyCardScene(feature_set),
    DialogCloseButtonScene(feature_set),
    DialogChoicesScene(feature_set),
    DialogPlayingScene(feature_set),
    BlackDialogScene(feature_set),
])

# Starting the UI overlay to begin automation
overlay.start()

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

# FeatureSet loads in-game UI elements from a COCO-format dataset for accurate automation
coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, hwnd_window.width, hwnd_window.height)

# Setup UI overlay for detection box display, optional
overlay = TkOverlay(hwnd_window, exit_event)

# TaskExecutor to manage the scenes and tasks
task_executor = TaskExecutor(capture, overlay=overlay, target_fps=30, exit_event=exit_event)

# Initializing interaction module for sending keyboard and mouse event to the game
interaction = Win32Interaction(capture, overlay)

# Adding automated tasks for gameplay, such as dialog navigation and item collection
task_executor.tasks.extend([
    AutoPlayDialogTask(interaction, feature_set),  # speeding up the dialogs
    AutoChooseDialogTask(interaction, feature_set),  # choose dialog options
    AutoPickTask(interaction, feature_set),  # pickup items in world scene
    AutoLoginTask(interaction, feature_set),  # auto login and claim reward
])

# Defining game scenes to handle different in-game situations through automated tasks
task_executor.scenes.extend([
    WorldScene(interaction, feature_set),
    StartScene(interaction, feature_set),
    MonthlyCardScene(interaction, feature_set),
    DialogCloseButtonScene(interaction, feature_set),
    DialogChoicesScene(interaction, feature_set),
    DialogPlayingScene(interaction, feature_set),
    BlackDialogScene(interaction, feature_set),
])

# Starting the UI overlay to begin automation
overlay.start()

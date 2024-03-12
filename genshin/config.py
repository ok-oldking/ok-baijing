from genshin.scene.BlackDialogScene import BlackDialogScene
from genshin.scene.DialogChoicesScene import DialogChoicesScene
from genshin.scene.DialogCloseButtonScene import DialogCloseButtonScene
from genshin.scene.DialogPlayingScene import DialogPlayingScene
from genshin.scene.MonthlyCardScene import MonthlyCardScene
from genshin.scene.WorldScene import WorldScene
from genshin.task.AutoChooseDialogTask import AutoChooseDialogTask
from genshin.task.AutoPickTask import AutoPickTask
from genshin.task.AutoPlayDialogTask import AutoPlayDialogTask

from scene.StartScence import StartScene
from task.AutoLoginTask import AutoLoginTask

config = {
    'debug': True,  # Optional, default: False
    'use_gui': True,  # Optional, default: False
    'capture': 'windows',  # adb/windows, see #autoui.capture
    'interaction': 'windows',  # adb/windows, see #autoui.interaction
    'capture_window_title': '原神',  # required  when using windows capture
    'default_horizontal_variance': 0,
    'default_vertical_variance': 0,
    'default_threshold': 0.95,
    'coco_feature_folder': 'assets/coco_feature',  # required if using feature detection
    'log_file': 'logs/auto_ui.log',  # Optional, auto rotating every day
    'tasks': [  # tasks to execute
        AutoPlayDialogTask(),  # speeding up the dialogs
        AutoChooseDialogTask(),  # choose dialog options
        AutoPickTask(),  # pickup items in world scene
        AutoLoginTask(),  # auto login and claim reward
    ], 'scenes': [  # scenes to detect
        WorldScene(),
        StartScene(),
        MonthlyCardScene(),
        DialogCloseButtonScene(),
        DialogChoicesScene(),
        DialogPlayingScene(),
        BlackDialogScene(),
    ]
}

from show_case_genshin.scene.BlackDialogScene import BlackDialogScene
from show_case_genshin.scene.DialogChoicesScene import DialogChoicesScene
from show_case_genshin.scene.DialogCloseButtonScene import DialogCloseButtonScene
from show_case_genshin.scene.DialogPlayingScene import DialogPlayingScene
from show_case_genshin.scene.MonthlyCardScene import MonthlyCardScene
from show_case_genshin.scene.StartScence import StartScene
from show_case_genshin.scene.WorldScene import WorldScene
from show_case_genshin.task.AutoChooseDialogTask import AutoChooseDialogTask
from show_case_genshin.task.AutoLoginTask import AutoLoginTask
from show_case_genshin.task.AutoPickTask import AutoPickTask
from show_case_genshin.task.AutoPlayDialogTask import AutoPlayDialogTask

config = {
    'debug': True,  # Optional, default: False
    'use_gui': True,  # Optional, default: False
    'capture': 'windows',  # adb/windows, see #autohelper.capture
    'interaction': 'windows',  # adb/windows, see #autohelper.interaction
    'capture_window_title': r"^(原神|Genshin Impact)$",  # required  when using windows capture
    'default_horizontal_variance': 0,
    'default_vertical_variance': 0,
    'default_threshold': 0.9,
    'coco_feature_folder': 'assets/coco_feature',  # required if using feature detection
    'log_file': 'logs/auto_helper.log',  # Optional, auto rotating every day
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

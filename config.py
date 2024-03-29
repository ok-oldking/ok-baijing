from task.ManXunTask import ManXunTask

config = {
    'debug': True,  # Optional, default: False
    'use_gui': True,
    'ocr': {
        'lang': 'ch'
    },
    'config_folder': 'configs',
    # 'gui_icon': 'icon.png',  # Optional
    'gui_title': 'BJ Helper',  # Optional, default: False
    'capture': 'adb',  # adb/windows, see #autohelper.capture
    'capture_window_title': 'Mumu Player 12',  # required  when using windows capture
    'interaction': 'adb',  # adb/windows, see #autohelper.interaction
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/auto_helper.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/auto_helper_error.log',
    'tasks': [  # tasks to execute
        ManXunTask(),
    ], 'scenes': [  # scenes to detect

    ]
}

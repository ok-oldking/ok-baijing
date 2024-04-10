from ok.util.path import get_path_in_package

from task.ManXunTask import ManXunTask

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': 'RapidOCR',
    'gui_title': 'OK白荆漫巡',  # Optional, default: False
    'capture': 'adb',  # adb/windows, see #ok.capture
    'capture_window_title': r'^白荆回廊\[[0-9.]+\]$',  # required  when using windows capture
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/auto_helper.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/auto_helper_error.log',
    'tasks': [  # tasks to execute
        ManXunTask(),
    ], 'scenes': [  # scenes to detect

    ]
}

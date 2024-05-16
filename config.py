from ok.util.path import get_path_in_package
from task.AoSkillManXunTask import AoSkillManXunTask

from task.ManXunTask import ManXunTask

version = "v0.0.1"

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': 'RapidOCR',
    'coco_feature_folder': 'assets/coco',  # required if using feature detection
    'about': """
    <h1>OK白荆回廊自动漫巡辅助</h1>
    <p>QQ群:594495691</p>
""",
    'screenshots_folder': "screenshots",
    'gui_title': 'OK白荆漫巡',  # Optional
    'capture_window_title': r'^白荆回廊\[[0-9.]+\]$',  # required  when using windows capture
    'capture_window_exe_name': 'GateMK-Win64-Shipping.exe',
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/ok-script.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/ok-script_error.log',
    'version': version,
    'onetime_tasks': [  # tasks to execute
        ManXunTask(),
        AoSkillManXunTask(),
    ], 'scenes': [  # scenes to detect

    ]
}

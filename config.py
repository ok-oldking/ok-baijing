import os
import re
from pathlib import Path

from ok.util.path import get_path_in_package
from task.AoSkillManXunTask import AoSkillManXunTask
from task.ManXunTask import ManXunTask

version = "v0.0.1"


def calculate_pc_exe_path(running_path):
    install_top = Path(running_path).parents[5]
    return str(install_top / "白荆回廊.lnk")


config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': {
        'lib': 'RapidOCR',
        'inference_num_threads': int(os.cpu_count() / 2)
    },
    'coco_feature_folder': os.path.join('assets', 'coco'),  # required if using feature detection
    'windows_capture': {  # required  when supporting windows game
        'title': re.compile(r'^白荆回廊'),
        'exe': 'GateMK-Win64-Shipping.exe',
        'calculate_pc_exe_path': calculate_pc_exe_path,
        'can_bit_blt': False  # default false, opengl games does not support bit_blt
    },
    'adb_capture': {

    },
    'about': """
    <h1>OK白荆回廊自动漫巡辅助</h1>
    <p>QQ群:594495691</p>
""",
    'supported_screen_ratio': '16:9',
    'screenshots_folder': "screenshots",
    'gui_title': 'OK白荆漫巡',  # Optional
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/ok-script.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/ok-script_error.log',
    'version': version,
    'locale': 'zh_CN',
    'onetime_tasks': [  # tasks to execute
        ManXunTask(),
        AoSkillManXunTask(),
    ], 'scenes': [  # scenes to detect

    ]
}

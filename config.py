import os
import re

from ok.util.path import get_path_in_package
from task.AoSkillManXunTask import AoSkillManXunTask
from task.AoSkillManXunTask2 import AoSkillManXunTask2
from task.AoSkillManXunTask3 import AoSkillManXunTask3
from task.AutoStartCombatTask import AutoStartCombatTask
from task.DailyTask import DailyTask
from task.JoinGameTask import JoinGameTask
from task.ManXunTask import ManXunTask

version = "v1.4.11"


def calculate_pc_exe_path(running_path):
    return None


config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': {
        'lib': 'RapidOCR',
        'inference_num_threads': int(os.cpu_count() / 2)
    },
    # required if using feature detection
    'template_matching': {
        'coco_feature_json': os.path.join('assets', 'result.json'),
        'default_horizontal_variance': 0.01,
        'default_vertical_variance': 0.01,
        'default_threshold': 0.9,
    },
    'windows': {  # required  when supporting windows game
        'title': re.compile(r'^白荆回廊'),
        'exe': 'GateMK-Win64-Shipping.exe',
        'calculate_pc_exe_path': calculate_pc_exe_path,
        # 'interaction': 'PostMessage',
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        'bit_blt_render_full': True
    },
    'adb': {
        'packages': ['com.tencent.gate']
    },
    'analytics': {
        'report_url': 'https://okreport.ok-script.com/report'
    },
    'update': {
        'releases_url': 'https://api.github.com/repos/ok-oldking/ok-baijing/releases?per_page=15',
        'proxy_url': 'https://gh.ok-script.com/',
        'exe_name': 'ok-baijing.exe',
        'use_proxy': True
    },
    'about': """
    <h3>OK白荆</h3>
    <p>免费开源软件 <a href="https://github.com/ok-oldking/ok-baijing">https://github.com/ok-oldking/ok-baijing</></p>
    <p>报告问题BUG <a href="https://github.com/ok-oldking/ok-baijing/issues/new?assignees=ok-oldking&labels=bug&projects=&template=%E6%8A%A5%E5%91%8Abug-.md&title=%5BBUG%5D">https://github.com/ok-oldking/ok-baijing/issues/new?assignees=ok-oldking&labels=bug&projects=&template=%E6%8A%A5%E5%91%8Abug-.md&title=%5BBUG%5D</></p>
    <p>视频演示 <a href="https://www.bilibili.com/video/BV1K7421f7KT/">https://www.bilibili.com/video/BV1K7421f7KT/</a></p>
    <p>QQ群:<a href="https://qm.qq.com/q/aGO7eBJ2Uw">594495691</a></p>
""",
    'supported_resolution': {
        'ratio': '16:9',
        'min_size': (1280, 720)
    },
    'supported_screen_ratio': '16:9',
    'screenshots_folder': "screenshots",
    'gui_title': 'OK白荆',  # Optional
    'log_file': 'logs/ok-script.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/ok-script_error.log',
    'version': version,
    'locale': 'zh_CN',
    'onetime_tasks': [  # tasks to execute
        DailyTask(),
        AoSkillManXunTask(),
        JoinGameTask(),
        AoSkillManXunTask2(),
        AoSkillManXunTask3(),
        ManXunTask(),
    ], 'trigger_tasks': [
        AutoStartCombatTask()
    ],
    'scenes': [  # scenes to detect

    ]
}

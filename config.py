import os
import re

from ok.util.path import get_path_in_package

version = "v5.4.11"


def calculate_pc_exe_path(running_path):
    return None


config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': {
        'lib': 'rapidocr_openvino'
        # 'lib': 'rapidocr_openvino'
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
    'git_update': {'sources': [{
        'name': 'Global',
        'git_url': 'https://github.com/ok-oldking/ok-baijing',
        'pip_url': 'https://pypi.org/simple/'
    }, {
        'name': 'China',
        'git_url': 'https://gitee.com/ok-olding/ok_baijing',
        'pip_url': 'https://mirrors.cloud.tencent.com/pypi/simple'
    }]},
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
        ['task.DailyTask', 'DailyTask'],
        ['task.JoinGameTask', 'JoinGameTask'],
    ], 'trigger_tasks': [
        ['task.AutoStartCombatTask', 'AutoStartCombatTask'],
    ]
}

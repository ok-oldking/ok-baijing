from ok.util.path import get_path_in_package

from task.ManXunTask import ManXunTask

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': get_path_in_package(__file__, 'icon.ico'),
    'ocr': 'RapidOCR',
    'about': """
    <h1>基于ok-script的白荆回廊自动漫巡辅助</h1>
    <p>Github下载和源码地址:</p>
    <p><a href="https://github.com/ok-oldking/ok_baijing">https://github.com/ok-oldking/ok_baijing</a></p>
""",
    'click_screenshots_folder': "click_screenshots",  # debug用 点击后截图文件夹
    'screenshots_folder': "screenshots",
    'gui_title': 'OK白荆漫巡',  # Optional
    'capture_window_title': r'^白荆回廊\[[0-9.]+\]$',  # required  when using windows capture
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/ok-script.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/ok-script_error.log',
    'onetime_tasks': [  # tasks to execute
        ManXunTask(),
    ], 'scenes': [  # scenes to detect

    ]
}

import re

from autohelper.AutoHelper import AutoHelper
from config import config

config = config
config['capture'] = 'windows'
config['capture_window_title'] = re.compile(r'^白荆回廊')
config['interaction'] = 'windows'
autoui = AutoHelper(config)

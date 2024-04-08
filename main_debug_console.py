from autohelper.AutoHelper import AutoHelper
from config import config

config = config
config['debug'] = True
config['use_gui'] = False
autoui = AutoHelper(config)

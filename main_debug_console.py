from config import config
from ok.OK import OK

config = config
config['debug'] = True
config['use_gui'] = False
autoui = OK(config)

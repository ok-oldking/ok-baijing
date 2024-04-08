from config import config
from ok.OK import OK

config = config
config['debug'] = True
autoui = OK(config)

from config import config
from ok.OK import OK

config = config
config['debug'] = True
ok = OK(config)
ok.start()

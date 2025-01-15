# flake8: noqa
from toolkit.settings_shared import *

try:
    from toolkit.local_settings import *
except ImportError:
    pass

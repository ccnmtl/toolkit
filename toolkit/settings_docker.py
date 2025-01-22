# flake8: noqa
from toolkit.settings_shared import *
from ctlsettings.docker import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))

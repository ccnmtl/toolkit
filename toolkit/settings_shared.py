# Django settings for toolkit project.
import os.path
from ctlsettings.shared import common

project = 'toolkit'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'toolkit.main',
]

USE_TZ = True

INSTALLED_APPS += [  # noqa
    'django_bootstrap5',
    'django_extensions',
    'toolkit',
    'toolkit.main',
    'contactus'
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7

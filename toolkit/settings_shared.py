# Django settings for toolkit project.
import os.path
from ctlsettings.shared import common

project = 'toolkit'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        # 'HOST': 'host.docker.internal',
        # # use this for Mac and Windows when the Postgres
        # is running in another Docker container outside the network
        'HOST': os.environ.get('JOBS_DB_HOST'),
        # use this for Linux when the Postgres is running
        # in another Docker container inside the network
        'PORT': 5432,
    }
}

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
CONTACT_US_EMAIL = "ctl-admin@columbia.edu"

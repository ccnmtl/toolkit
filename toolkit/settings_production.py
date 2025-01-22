from ctlsettings.production import common, init_sentry
from toolkit.settings_shared import *  # noqa: F403
from django.conf import settings
import os


locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        # if you use cloudfront:
        #        cloudfront="justtheidhere",
        # if you don't use S3/cloudfront at all:
        # s3static=False,
    ))

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

SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_KEY = os.environ.get('SENTRY_KEY')

if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405

from toolkit.settings_shared import *  # noqa: F403
from ctlsettings.staging import common, init_sentry
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


SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_KEY = os.environ.get('SENTRY_KEY')

if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405

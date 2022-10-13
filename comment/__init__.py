import django
from django.conf import settings as django_settings
from django.utils.functional import LazyObject
from comment import settings as app_settings


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings(app_settings, django_settings)


class Settings(object):
    DEPRECATED_SETTINGS = {
        'PASSWORD_RESET_TIMEOUT_DAYS' if django.VERSION > (3, 0) else None,
        'DEFAULT_CONTENT_TYPE' if django.VERSION > (2, 2) else None,
        'FILE_CHARSET' if django.VERSION > (2, 2) else None,
        'USE_L10N' if django.VERSION > (4, 0) else None,
        'USE_TZ' if django.VERSION > (4, 0) else None,
    }

    def __init__(self, *args):
        for item in args:
            for attr in dir(item):
                if attr.isupper() and attr not in self.DEPRECATED_SETTINGS:
                    setattr(self, attr, getattr(item, attr))


settings = LazySettings()

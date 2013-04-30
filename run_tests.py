import sys
from django.conf import settings


def main():
    # Configure django
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'chunkycms',
        ],
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MEDIA_ROOT='/tmp/media/',
        MEDIA_PATH='/media/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
        ),
        TEMPLATE_DIRS = ('tests/templates/',),
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        USE_TZ=True,
    )

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['chunkycms'])
    sys.exit(failures)

if __name__ == '__main__':
    main()

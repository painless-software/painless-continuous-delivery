"""
Django settings for application project.
"""
from pathlib import Path

from environ import Env

env = Env()  # pylint: disable=invalid-name

ENVIRONMENT = env('ENVIRONMENT', default='local')
REVISION = env('REVISION', default=None)
{%- if cookiecutter.monitoring == 'Sentry' %}
SENTRY_DSN = env('SENTRY_DSN', default=None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT,
        release=REVISION)
{%- endif %}

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = 'dummy-secret' if DEBUG else env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*'] if DEBUG else [
{%- if cookiecutter.production_domain != '(automatic)' %}
    '.{{ cookiecutter.production_domain }}',
{%- else %}
    # '.your.example.com',
{%- endif %}
{%- if cookiecutter.cloud_platform == 'APPUiO' %}
    '.appuioapp.ch',
{%- endif %}
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    {%- if cookiecutter.monitoring == 'Datadog' %}
    'django_datadog',
    {%- endif %}
    'django_probes',
]

MIDDLEWARE = [
    {%- if cookiecutter.monitoring == 'Datadog' %}
    'django_datadog.middleware.DatadogMiddleware',
    {%- endif %}
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'

# Database

DATABASES = {
    'default': env.db(
        'DJANGO_DATABASE_URL',
        {%- if cookiecutter.database == '(none)' %}
        default='sqlite://%s' % join(BASE_DIR, 'db.sqlite3')
        {%- elif cookiecutter.database == 'Postgres' %}
        default='postgres://postgres:postgres@database/postgres'
        {%- elif cookiecutter.database == 'MySQL' %}
        default='mysql://mysql:mysql@database/mysql'
        {%- endif %}
    ),
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TEMPLATE_CONTEXT': True,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ['debug_toolbar']

if SECRET_KEY == 'testing':
    INSTALLED_APPS += ['behave_django']
{%- if cookiecutter.monitoring == 'Datadog' %}

DATADOG_API_KEY = env('DATADOG_API_KEY', default=None)
DATADOG_APP_KEY = env('DATADOG_APP_KEY', default=None)
DATADOG_APP_NAME = env('DATADOG_APP_NAME', default=None)
{%- elif cookiecutter.monitoring == 'NewRelic' %}

NEWRELIC_LICENSE_KEY = env('NEWRELIC_LICENSE_KEY', default=None)

if NEWRELIC_LICENSE_KEY:
    import newrelic.agent

    newrelic.agent.initialize(join(BASE_DIR, 'newrelic.ini'))
{%- endif %}

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

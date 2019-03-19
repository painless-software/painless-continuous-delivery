"""
Django settings for application project.
"""
from os.path import abspath, dirname, join
from environ import Env

BASE_DIR = dirname(dirname(abspath(__file__)))

env = Env()  # pylint: disable=invalid-name
Env.read_env(join(BASE_DIR, '.env'))

DEBUG = env.bool('DJANGO_DEBUG', default=True)

SECRET_KEY = 'dummy-secret' if DEBUG else env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
] if DEBUG else [
    'example.com',
]

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
    {%- elif cookiecutter.monitoring == 'Sentry' %}
    'raven.contrib.django.raven_compat',
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
{%- elif cookiecutter.database == 'MySQL/MariaDB' %}
        default='mysql://mysql:mysql@database/mysql'
{%- endif %}
    ),
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
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
{%- if cookiecutter.monitoring == 'Datadog' %}

DATADOG_API_KEY = env('DATADOG_API_KEY', default=None)
DATADOG_APP_KEY = env('DATADOG_APP_KEY', default=None)
DATADOG_APP_NAME = env('DATADOG_APP_NAME', default=None)
{%- elif cookiecutter.monitoring == 'Sentry' %}

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN', default=None),
    # Automatically configure the release based on information from Git
    'release': env('REVISION', default=None),
}
{%- endif %}

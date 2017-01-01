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

ALLOWED_HOSTS = [] if DEBUG else [
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
]

MIDDLEWARE = [
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
    'default': {
{%- if cookiecutter.database == '(none)' %}
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
{%- elif cookiecutter.database == 'Postgres' %}
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DATABASE', default='postgres'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default=None),
        'HOST': env('POSTGRES_HOST', default='database'),
        'PORT': env.int('POSTGRES_PORT', default=5432),
{%- elif cookiecutter.database == 'MySQL/MariaDB' %}
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MYSQL_DATABASE', default='mysql'),
        'USER': env('MYSQL_USER', default='mysql'),
        'PASSWORD': env('MYSQL_PASSWORD', default='mysql'),
        'HOST': env('MYSQL_HOST', default='database'),
        'PORT': env.int('MYSQL_PORT', default=3306),
{%- endif %}
    }
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

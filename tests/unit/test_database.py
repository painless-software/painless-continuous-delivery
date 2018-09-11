"""Tests for correctly generated database configurations."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import verify_required_settings


# pylint: disable=too-few-public-methods
class TestDatabase(object):
    """
    Tests for verifying database configuration in generated projects.
    """
    scenarios = [
        ('(none)', {
            'project_slug': 'django-project-no-db',
            'framework': 'Django',
            'database': '(none)',
            'required_settings': {
                'DATABASES': {
                    'ENGINE': "'django.db.backends.sqlite3'",
                    'NAME': "join(BASE_DIR, 'db.sqlite3')",
                }
            },
            'required_packages': [
                'django-environ',
            ],
        }),
        ('Postgres', {
            'project_slug': 'django-project-postgres',
            'framework': 'Django',
            'database': 'Postgres',
            'required_settings': {
                'DATABASES': {
                    'ENGINE': "'django.db.backends.postgresql'",
                    'NAME': "env('POSTGRES_DATABASE', default='postgres')",
                    'USER': "env('POSTGRES_USER', default='postgres')",
                    'PASSWORD': "env('POSTGRES_PASSWORD', default=None)",
                    'HOST': "env('POSTGRES_HOST', default='database')",
                    'PORT': "env.int('POSTGRES_PORT', default=5432)",
                },
            },
            'required_packages': [
                'django-environ',
                'psycopg2-binary',
            ],
        }),
        ('MySQL/MariaDB', {
            'project_slug': 'django-project-mysql',
            'framework': 'Django',
            'database': 'MySQL/MariaDB',
            'required_settings': {
                'DATABASES': {
                    'ENGINE': "'django.db.backends.mysql'",
                    'NAME': "env('MYSQL_DATABASE', default='mysql')",
                    'USER': "env('MYSQL_USER', default='mysql')",
                    'PASSWORD': "env('MYSQL_PASSWORD', default='mysql')",
                    'HOST': "env('MYSQL_HOST', default='database')",
                    'PORT': "env.int('MYSQL_PORT', default=3306)",
                },
            },
            'required_packages': [
                'django-environ',
                'mysqlclient',
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_database(self, cookies, project_slug, framework, database,
                      required_settings, required_packages):
        """
        Generate a project and verify its database configuration everywhere.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'database': database,
        })

        assert result.exit_code == 0
        assert result.exception is None

        settings = result.project.join(
            'application', 'settings.py').readlines(cr=False)
        verify_required_settings(required_settings, settings)

        requirements_txt = \
            result.project.join('requirements.txt').readlines(cr=False)
        for req in required_packages:
            assert req in requirements_txt

        assert result.project.join('tox.ini').isfile()
        with result.project.as_cwd():
            exit_code = system('flake8')
            assert exit_code == 0, 'PEP8 violation or syntax error.' \
                                   ' (flake8 failed; see captured stdout call)'

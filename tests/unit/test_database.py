"""Tests for correctly generated database configurations."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


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
                'ENGINE': 'django.db.backends.sqlite3',
            },
            'required_packages': [],
        }),
        ('Postgres', {
            'project_slug': 'django-project-postgres',
            'framework': 'Django',
            'database': 'Postgres',
            'required_settings': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'postgres',
                'USER': 'postgres',
                'HOST': 'database',
                'PORT': 5432,
            },
            'required_packages': [
                'psycopg2',
            ],
        }),
        ('MySQL/MariaDB', {
            'project_slug': 'django-project-mysql',
            'framework': 'Django',
            'database': 'MySQL/MariaDB',
            'required_settings': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'mysql',
                'USER': 'mysql',
                'HOST': 'database',
                'PORT': 3306,
            },
            'required_packages': [
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

        settings_file = result.project.join('application', 'settings.py')
        settings = settings_file.pyimport(str(settings_file.pypkgpath()))
        db_settings = settings.DATABASES['default']
        for key, value in required_settings.items():
            assert db_settings[key] == value

        requirements_txt = \
            result.project.join('requirements.txt').readlines(cr=False)
        for req in required_packages:
            assert req in requirements_txt

        exit_code = system('flake8 %s' % result.project.dirname)
        assert exit_code == 0, 'PEP8 violation or syntax error.' \
                               ' (flake8 failed; see captured stdout call)'

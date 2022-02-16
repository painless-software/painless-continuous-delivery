"""
Tests for correctly generated database configurations.
"""

from cli_test_helpers import shell

from .helpers import (  # noqa, pylint: disable=unused-import
    FunctionCall,
    dedent,
    indent2,
    pytest_generate_tests,
    verify_required_settings,
)


# pylint: disable=too-few-public-methods
class TestDatabase:
    """
    Tests for verifying database configuration in generated projects.
    """
    env_db = FunctionCall('env.db')
    scenarios = [
        ('(none)', {
            'project_slug': 'django-project-no-db',
            'framework': 'Django',
            'database': '(none)',
            'required_settings': {
                'DATABASES': {
                    'default': env_db(
                        "'DJANGO_DATABASE_URL',",
                        'default=f"sqlite://{BASE_DIR / \'db.sqlite3\'}"',
                    ),
                },
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
                    'default': env_db(
                        "'DJANGO_DATABASE_URL',",
                        "default='postgres://"
                        "postgres:postgres@database/postgres'",
                    ),
                },
            },
            'required_packages': [
                'django-environ',
                'psycopg2',
            ],
        }),
        ('MySQL', {
            'project_slug': 'django-project-mysql',
            'framework': 'Django',
            'database': 'MySQL',
            'required_settings': {
                'DATABASES': {
                    'default': env_db(
                        "'DJANGO_DATABASE_URL',",
                        "default='mysql://mysql:mysql@database/mysql'",
                    ),
                },
            },
            'required_packages': [
                'django-environ',
                'mysql-connector',
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

        settings = (
            result.project_path / 'application' / 'settings.py'
        ).read_text().splitlines()
        verify_required_settings(required_settings, settings)

        requirements_txt = (
            result.project_path / 'requirements.in'
        ).read_text().splitlines()
        for req in required_packages:
            assert req in requirements_txt

        assert (result.project_path / 'tox.ini').is_file()

        run = shell('flake8', cwd=result.project_path)
        # pylint: disable=no-member
        assert run.exit_code == 0, \
            'PEP8 violation or syntax error. ' \
            '(flake8 failed; see captured stdout call)'

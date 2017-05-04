"""Tests for correctly generated monitoring configurations."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import slice_dict_from


# pylint: disable=too-few-public-methods
class TestMonitoring(object):
    """
    Tests for verifying monitoring configuration in generated projects.
    """
    scenarios = [
        ('Sentry(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'Sentry',
            'required_settings': {
                'dsn': "env('SENTRY_DSN', default=None)",
                'release': "env('REVISION', default=None)",
            },
            'required_packages': [
                'raven',
            ],
        }),
        # ('Sentry(flask)', {
        #     'project_slug': 'flask-project',
        #     'framework': 'Flask',
        #     'monitoring': 'Sentry',
        #     'required_settings': {
        #         'dsn': "env('SENTRY_DSN', default=None)",
        #         'release': "raven.fetch_git_sha(dirname(pardir))",
        #     },
        #     'required_packages': [
        #         'raven',
        #     ],
        # }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_monitoring(self, cookies, project_slug, framework, monitoring,
                        required_settings, required_packages):
        """
        Generate a project and verify its monitoring configuration everywhere.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'monitoring': monitoring,
        })

        assert result.exit_code == 0
        assert result.exception is None

        settings = result.project.join(
            'application', 'settings.py').readlines(cr=False)
        db_settings = slice_dict_from('RAVEN_CONFIG', settings)
        for key, value in required_settings.items():
            key_value_pair = "'%s': %s," % (key, value)
            assert key_value_pair in db_settings

        requirements_txt = \
            result.project.join('requirements.txt').readlines(cr=False)
        for req in required_packages:
            assert req in requirements_txt

        exit_code = system('flake8 %s' % result.project.dirname)
        assert exit_code == 0, 'PEP8 violation or syntax error.' \
                               ' (flake8 failed; see captured stdout call)'

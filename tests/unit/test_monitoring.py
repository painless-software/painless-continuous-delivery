"""
Tests for correctly generated monitoring configurations.
"""
from os import system

from . import (  # noqa, pylint: disable=unused-import
    pytest_generate_tests,
    verify_required_settings,
)


# pylint: disable=too-few-public-methods
class TestMonitoring:
    """
    Tests for verifying monitoring configuration in generated projects.
    """
    scenarios = [
        ('Datadog(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'Datadog',
            'required_settings': {
                'MIDDLEWARE': [
                    "'django_datadog.middleware.DatadogMiddleware',",
                ],
                'DATADOG_API_KEY': "env('DATADOG_API_KEY', default=None)",
                'DATADOG_APP_KEY': "env('DATADOG_APP_KEY', default=None)",
                'DATADOG_APP_NAME': "env('DATADOG_APP_NAME', default=None)",
            },
            'required_packages': [
                'django-datadog',
            ],
        }),
        ('NewRelic(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'NewRelic',
            'required_settings': {
                'NEWRELIC_LICENSE_KEY':
                "env('NEWRELIC_LICENSE_KEY', default=None)",
            },
            'required_packages': [
                'newrelic',
            ],
        }),
        ('Sentry(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'Sentry',
            'required_settings': {
                'SENTRY_DSN': "env('SENTRY_DSN', default=None)",
            },
            'required_packages': [
                'sentry-sdk',
            ],
        }),
        # ('Sentry(flask)', {
        #     'project_slug': 'flask-project',
        #     'framework': 'Flask',
        #     'monitoring': 'Sentry',
        #     'required_settings': {
        #         'SENTRY_DSN': "env('SENTRY_DSN', default=None)",
        #     },
        #     'required_packages': [
        #         'sentry-sdk',
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
        verify_required_settings(required_settings, settings)

        requirements_txt = result.project.join(
            'requirements.in').readlines(cr=False)
        for req in required_packages:
            assert req in requirements_txt

        assert result.project.join('tox.ini').isfile()
        with result.project.as_cwd():
            exit_code = system('flake8')
            assert exit_code == 0, 'PEP8 violation or syntax error.' \
                                   ' (flake8 failed; see captured stdout call)'

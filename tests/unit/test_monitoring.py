"""
Tests for correctly generated monitoring configurations.
"""
from os import system

from .helpers import (  # noqa, pylint: disable=unused-import
    dedent,
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
            'cloud_platform': 'APPUiO',
            'docker_registry': 'registry.appuio.ch',
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
            'required_content': [
                ('README.rst', [
                    dedent("""
                    Integrate External Tools
                    ^^^^^^^^^^^^^^^^^^^^^^^^

                    :Datadog:
                      - Add environment variables ``DATADOG_API_KEY``, \
``DATADOG_APP_KEY``, ``DATADOG_APP_NAME`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/django-project/-/settings/ci_cd>`__
                      - Delete secrets in your namespace and run a deployment \
(to recreate them)

                    """),
                ]),
            ],
        }),
        ('NewRelic(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'NewRelic',
            'cloud_platform': 'APPUiO',
            'docker_registry': 'registry.appuio.ch',
            'required_settings': {
                'NEWRELIC_LICENSE_KEY':
                "env('NEWRELIC_LICENSE_KEY', default=None)",
            },
            'required_packages': [
                'newrelic',
            ],
            'required_content': [
                ('README.rst', [
                    dedent("""
                    Integrate External Tools
                    ^^^^^^^^^^^^^^^^^^^^^^^^

                    :New Relic:
                      - Add environment variable ``NEWRELIC_LICENSE_KEY`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/django-project/-/settings/ci_cd>`__
                      - Delete secrets in your namespace and run a deployment \
(to recreate them)

                    """),
                ]),
            ],
        }),
        ('NewRelic(flask)', {
            'project_slug': 'flask-project',
            'framework': 'Flask',
            'monitoring': 'NewRelic',
            'cloud_platform': 'Rancher',
            'docker_registry': 'nexus.example.com',
            'required_settings': None,
            'required_packages': [
                'newrelic',
            ],
            'required_content': [
                ('README.rst', [
                    dedent("""
                    Integrate External Tools
                    ^^^^^^^^^^^^^^^^^^^^^^^^

                    :New Relic:
                      - Add environment variable ``NEWRELIC_LICENSE_KEY`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/flask-project/-/settings/ci_cd>`__
                      - Delete secrets in your namespace and run a deployment \
(to recreate them)
                    """),
                ]),
            ],
        }),
        ('Sentry(django)', {
            'project_slug': 'django-project',
            'framework': 'Django',
            'monitoring': 'Sentry',
            'cloud_platform': 'APPUiO',
            'docker_registry': 'registry.gitlab.com',
            'required_settings': {
                'SENTRY_DSN': "env('SENTRY_DSN', default=None)",
            },
            'required_packages': [
                'sentry-sdk',
            ],
            'required_content': [
                ('README.rst', [
                    dedent("""
                    Integrate External Tools
                    ^^^^^^^^^^^^^^^^^^^^^^^^

                    :Sentry:
                      - Add environment variable ``SENTRY_DSN`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/django-project/-/settings/ci_cd>`__
                      - Delete secrets in your namespace and run a deployment \
(to recreate them)
                      - Configure `Error Tracking \
<https://gitlab.com/company-or-username/django-project/-/error_tracking>`__
                        in `Settings > Operations > Error Tracking \
<https://gitlab.com/company-or-username/django-project/-/settings/operations>`__

                    """),
                ]),
            ],
        }),
        ('Sentry(flask)', {
            'project_slug': 'flask-project',
            'framework': 'Flask',
            'monitoring': 'Sentry',
            'cloud_platform': 'Rancher',
            'docker_registry': 'nexus.example.com',
            'required_settings': None,
            'required_packages': [
                'sentry-sdk[flask]',
            ],
            'required_content': [
                ('application/__init__.py', [
                    dedent("""
                    import os
                    import sentry_sdk
                    from sentry_sdk.integrations.flask import FlaskIntegration

                    sentry_sdk.init(
                        dsn=os.environ.get('SENTRY_DSN'),
                        integrations=[FlaskIntegration()]
                    )
                    """),
                ]),
                ('README.rst', [
                    dedent("""
                    Integrate External Tools
                    ^^^^^^^^^^^^^^^^^^^^^^^^

                    :Sentry:
                      - Add environment variable ``SENTRY_DSN`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/flask-project/-/settings/ci_cd>`__
                      - Delete secrets in your namespace and run a deployment \
(to recreate them)
                      - Configure `Error Tracking \
<https://gitlab.com/company-or-username/flask-project/-/error_tracking>`__
                        in `Settings > Operations > Error Tracking \
<https://gitlab.com/company-or-username/flask-project/-/settings/operations>`__
                    :Image Registry:
                      - Add environment variable ``REGISTRY_PASSWORD`` in
                        `Settings > CI/CD > Variables \
<https://gitlab.com/company-or-username/flask-project/-/settings/ci_cd>`__

                    """),
                ]),
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_monitoring(self, cookies, project_slug, framework, monitoring,
                        cloud_platform, docker_registry, required_settings,
                        required_packages, required_content):
        """
        Generate a project and verify its monitoring configuration everywhere.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'monitoring': monitoring,
            'cloud_platform': cloud_platform,
            'docker_registry': docker_registry,
        })

        assert result.exit_code == 0
        assert result.exception is None
        readme_file = result.project.join('README.rst')
        assert readme_file.isfile()

        readme_content = '\n'.join(readme_file.readlines(cr=False))
        assert '\n\n\n' not in readme_content, \
            f"Excessive newlines in README: {readme_file}\n" \
            f"-------------\n{readme_content}"

        if required_settings:
            settings = result.project.join(
                'application', 'settings.py').readlines(cr=False)
            verify_required_settings(required_settings, settings)

        requirements_txt = result.project.join(
            'requirements.in').readlines(cr=False)
        for req in required_packages:
            assert req in requirements_txt

        for filename, chunks in required_content:
            file_content = result.project.join(filename).read()
            for chunk in chunks:
                assert chunk in file_content, \
                    'Not found in generated file %s:\n"%s"\n' \
                    '-----------\n%s' % \
                    (filename, chunk, file_content)

        assert result.project.join('tox.ini').isfile()
        with result.project.as_cwd():
            exit_code = system('flake8')
            assert exit_code == 0, 'PEP8 violation or syntax error.' \
                                   ' (flake8 failed; see captured stdout call)'

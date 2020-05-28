"""Tests for generating a testing setup for a project."""
from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import verify_file_matches_repo_root


# pylint: disable=too-few-public-methods
class TestTestingSetup:
    """
    Tests for verifying generated projects using specific Web frameworks.
    """
    scenarios = [
        ('django', {
            'project_slug': 'django-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Django',
            'checks': 'flake8,pylint',
            'tests': 'py35,py36,py37,pypy3,behave',
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    'envlist = flake8,pylint,py35,py36,py37,pypy3,behave',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:pylint]',
                    '    pylint-django',
                    '[flake8]',
                    '[pylint]',
                    '[MASTER]',
                    'load-plugins = pylint_django',
                    '[pytest]',
                ]),
            ],
            'match_project_root': [
                'tests/README.rst',
            ]
        }),
        ('flask', {
            'project_slug': 'flask-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Flask',
            'checks': '',
            'tests': 'py36,py37,behave',
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    'envlist = py36,py37,behave',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:pylint]',
                    '    pylint',
                    '[flake8]',
                    '[pylint]',
                    '[MASTER]',
                    '[pytest]',
                ]),
            ],
            'match_project_root': [
                'tests/README.rst',
            ]
        }),
        ('symfony', {
            'project_slug': 'symfony-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Symfony',
            'checks': 'phpcs,twig',
            'tests': 'phpunit',
            'test_configuration': [
                ('composer.json', [
                    '        "check": [\n'
                    '            "@composer phpcs",\n'
                    '            "@composer twig"\n'
                    '        ],',
                    '        "test": [\n'
                    '            "@composer phpunit"\n'
                    '        ],',
                ]),
            ],
            'match_project_root': [
            ]
        }),
        ('typo3', {
            'project_slug': 'typo3-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'TYPO3',
            'checks': 'phpcs',
            'tests': 'phpunit',
            'test_configuration': [
                ('composer.json', [
                ]),
            ],
            'match_project_root': [
            ]
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_testing(self, cookies, project_slug, vcs_account, vcs_platform,
                     ci_service, framework, checks, tests, test_configuration,
                     match_project_root):
        """
        Generate a project with a testing setup and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'framework': framework,
            'checks': checks,
            'tests': tests,
        })

        assert result.exit_code == 0
        assert result.exception is None

        for filename, expected_content in test_configuration:
            config_file = result.project.join(filename).read()
            for config_value in expected_content:
                assert config_value in config_file, \
                    'Configuration value missing in {filename}: {value}\n' \
                    '--------------- (content follows)\n' \
                    '{content}'.format(
                        filename=filename,
                        content=config_file,
                        value=config_value,
                    )

        # ensure this project itself stays up-to-date with the template
        for filename in match_project_root:
            verify_file_matches_repo_root(result, filename,
                                          max_compare_bytes=375)

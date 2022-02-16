"""
Tests for generating a testing setup for a project.
"""
from .helpers import (  # noqa, pylint: disable=unused-import
    pytest_generate_tests,
    verify_file_matches_repo_root,
)


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
            'ci_service': 'codeship-steps.yml',
            'framework': 'Django',
            'checks': 'flake8,pylint,isort',
            'tests': 'py38,pypy3,behave',
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    'envlist = flake8,pylint,isort,py38,pypy3,behave',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:isort]',
                    '[testenv:pylint]',
                    '    pylint-django',
                    '[flake8]',
                ]),
                ('pyproject.toml', [
                    '[tool.pylint.master]',
                    'load-plugins = "pylint_django"',
                    '[tool.pytest.ini_options]',
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
            'ci_service': 'codeship-steps.yml',
            'framework': 'Flask',
            'checks': 'isort',
            'tests': 'py38,behave',
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    'envlist = isort,py38,behave',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:isort]',
                    '[testenv:pylint]',
                    '    pylint',
                    '[flake8]',
                ]),
                ('pyproject.toml', [
                    '[tool.pylint.master]',
                    '[tool.pytest.ini_options]',
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
            'ci_service': 'codeship-steps.yml',
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
            'ci_service': 'codeship-steps.yml',
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
                    f'Config value missing in {filename}: {config_value}\n' \
                    '--------------- (content follows)\n' \
                    f'{config_file}'

        # ensure this project itself stays up-to-date with the template
        for filename in match_project_root:
            verify_file_matches_repo_root(result, filename,
                                          max_compare_bytes=1250)

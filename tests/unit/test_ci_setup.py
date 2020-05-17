"""Tests for generating a continuous integration setup."""
from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import verify_file_matches_repo_root


# pylint: disable=too-few-public-methods
class TestCISetup:
    """
    Tests for verifying generated CI setups of this cookiecutter,
    executed several times with different values (test scenarios).
    """
    scenarios = [
        ('bitbucket-shared', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'bitbucket-pipelines.yml',
            'ci_testcommand': '        - tox -e py37',
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'expected_ci_target':
                '        TARGET=myproject',
        }),
        ('bitbucket-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'bitbucket-pipelines.yml',
            'ci_testcommand': '        - tox -e py37',
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'expected_ci_target':
                '        TARGET=myproject-${BITBUCKET_DEPLOYMENT_ENVIRONMENT}',
        }),
        ('codeship', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': 'codeship-steps.yml',
            'ci_testcommand': '  service: app',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'expected_ci_target': '',
        }),
        ('gitlab-shared', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'ci_testcommand': '  script: tox -e py37',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'expected_ci_target':
                '  TARGET: myproject',
        }),
        ('gitlab-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'ci_testcommand': '  script: tox -e py37',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'expected_ci_target':
                '    TARGET: myproject-production',
        }),
        ('shippable', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'shippable.yml',
            'ci_testcommand': '  - tox',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'expected_ci_target': '',
        }),
        ('travis', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'ci_testcommand': 'script: tox',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'expected_ci_target': '',
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_ci_setup(self, cookies, project_slug, vcs_account, vcs_platform,
                      ci_service, ci_testcommand, checks, tests,
                      cloud_platform, environment_strategy,
                      expected_ci_target):
        """
        Generate a CI setup with specific settings and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'checks': checks,
            'tests': tests,
            'cloud_platform': cloud_platform,
            'environment_strategy': environment_strategy,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == project_slug
        assert result.project.isdir()
        assert result.project.join('README.rst').isfile()

        ci_service_conf = result.project.join(ci_service).readlines(cr=False)
        assert ci_testcommand in ci_service_conf, \
            "Test command not found in CI config: '%s'" % ci_testcommand
        assert expected_ci_target in ci_service_conf, \
            "Deployment target not found in CI config: '%s'\n%s" \
            % (expected_ci_target, '\n'.join(ci_service_conf))

        codeship_services = result.project.join('codeship-services.yml')
        assert (ci_service == 'codeship-steps.yml' and
                codeship_services.isfile()) or not codeship_services.exists()

        # ensure this project itself stays up-to-date with the template
        verify_file_matches_repo_root(result, ci_service,
                                      max_compare_bytes=85)

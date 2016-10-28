"""Tests for generating a continuous integration setup."""
from filecmp import cmp as compare_files

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import REPO_ROOT_PATH


# pylint: disable=too-few-public-methods
class TestCISetup(object):
    """
    Tests for verifying generated CI setups of this cookiecutter,
    executed several times with different values (test scenarios).
    """
    scenarios = [
        ('bitbucket', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'vcs_remote': 'git@bitbucket.org:painless-software/myproject.git',
            'ci_service': 'bitbucket-pipelines.yml',
            'ci_testcommand': '          - tox',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
        ('codeship', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'vcs_remote': 'git@bitbucket.org:painless-software/myproject.git',
            'ci_service': 'codeship-steps.yml',
            'ci_testcommand': '  service: app',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
        ('gitlab', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'vcs_remote': 'git@gitlab.com:painless-software/myproject.git',
            'ci_service': '.gitlab-ci.yml',
            'ci_testcommand': '  script: tox',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
        ('shippable', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'vcs_remote': 'git@bitbucket.org:painless-software/myproject.git',
            'ci_service': 'shippable.yml',
            'ci_testcommand': '    - tox',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
        ('travis', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'vcs_remote': 'git@github.com:painless-software/myproject.git',
            'ci_service': '.travis.yml',
            'ci_testcommand': 'script: tox',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
        ('vexor', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'vcs_remote': 'git@github.com:painless-software/myproject.git',
            'ci_service': 'vexor.yml',
            'ci_testcommand': 'script: tox',
            'tests': 'flake8,pylint,py27,py33,py34,py35,pypy',
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_ci_setup(self, cookies, project_slug,
                      vcs_account, vcs_platform, vcs_remote,
                      ci_service, ci_testcommand, tests):
        """
        Generate a CI setup with specific settings and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'tests': tests,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == project_slug
        assert result.project.isdir()
        assert result.project.join('README.rst').isfile()
        assert result.project.join('tests', 'requirements.txt').isfile()

        assert result.project.join('.git').isdir()
        assert result.project.join('.gitignore').isfile()
        git_config = result.project.join('.git', 'config').readlines(cr=False)
        assert '[remote "origin"]' in git_config
        assert '\turl = {}'.format(vcs_remote) in git_config

        tox_ini = result.project.join('tox.ini').readlines(cr=False)
        assert '[tox]' in tox_ini
        assert 'envlist = {}'.format(tests) in tox_ini
        assert '[testenv]' in tox_ini
        assert '[testenv:flake8]' in tox_ini
        assert '[testenv:pylint]' in tox_ini

        ci_service_conf = result.project.join(ci_service).readlines(cr=False)
        assert ci_testcommand in ci_service_conf

        codeship_services = result.project.join('codeship-services.yml')
        assert (ci_service == 'codeship-steps.yml' and
                codeship_services.isfile()) or not codeship_services.exists()

        # ensure this project itself stays up-to-date with the template
        file_list = ['.gitignore', 'tox.ini', ci_service]
        for filename in file_list:
            mother_file = REPO_ROOT_PATH.join(filename).strpath
            generated_file = result.project.join(filename).strpath
            assert compare_files(mother_file, generated_file), \
                "Mother project '{}' not matching template.\n {} != {}".format(
                    filename, mother_file, generated_file)

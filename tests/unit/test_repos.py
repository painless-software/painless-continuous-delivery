"""
Tests for generating a local Git repository and Docker registry setup.
"""
from .helpers import (  # noqa, pylint: disable=unused-import
    pytest_generate_tests,
)


# pylint: disable=too-few-public-methods
class TestRepos:
    """
    Tests for verifying generated local Git repository and Docker registry
    setup, executed several times with different values (test scenarios).
    """
    scenarios = [
        ('Bitbucket/DockerHub', {
            'project_slug': 'custom-app',
            'vcs_project': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'vcs_remote': 'git@bitbucket.org:painless-software/myproject.git',
            'ci_service': 'bitbucket-pipelines.yml',
            'docker_registry': 'hub.docker.com/painless-software',
        }),
        ('GitHub/Quay.io', {
            'project_slug': 'custom-app',
            'vcs_project': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'vcs_remote': 'git@github.com:painless-software/myproject.git',
            'ci_service': 'codeship-steps.yml',
            'docker_registry': 'quay.io/painless-software',
        }),
        ('GitLab/Registry', {
            'project_slug': 'custom-app',
            'vcs_project': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'vcs_remote': 'git@gitlab.com:painless-software/myproject.git',
            'ci_service': '.gitlab-ci.yml',
            'docker_registry': 'registry.gitlab.com/painless-software',
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_repos(self, cookies, project_slug, vcs_project, vcs_account,
                   vcs_platform, vcs_remote, ci_service, docker_registry):
        """
        Generate a Git repository ready to push, and a Docker setup
        referencing images on a Docker container registry service.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_project': vcs_project,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'docker_registry': docker_registry,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project_path.name == project_slug
        assert result.project_path.is_dir()

        assert (result.project_path / '.git').is_dir()
        git_config = \
            (result.project_path / '.git' / 'config').read_text().splitlines()
        remote_section = '[remote "origin"]'
        remote_url = f'\turl = {vcs_remote}'

        needle = remote_section
        haystack = '\n'.join(git_config)
        assert remote_section in git_config, \
            f'Remote declaration not found in .git/config: {needle}\n' \
            f'{haystack}'

        needle = remote_url
        haystack = '\n'.join(git_config)
        assert remote_url in git_config, \
            f'Remote URL not found in .git/config: {needle}\n' \
            f'{haystack}'

"""Tests for the GitOps deployment strategy."""
from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


# pylint: disable=too-few-public-methods
class TestGitops:
    """
    Tests for verifying generated projects deployed using GitOps.
    """
    scenarios = [
        ('Pipeline', {
            'deployment_strategy': 'pipeline',
            'project_slug': 'monolith',
            'framework': 'SpringBoot',
            'files_present': [
                'monolith/.git/config',
                'monolith/.gitignore',
                'monolith/deployment/application/base/kustomization.yaml',
                'monolith/deployment/database/base/kustomization.yaml',
                'monolith/deployment/webserver/',
                'monolith/docker-compose.yml',
                'monolith/Dockerfile',
                'monolith/README.rst',
            ],
            'files_absent': [
                'monolith/gitops/',
                'monolith-gitops/',
            ],
        }),
        ('GitOps', {
            'deployment_strategy': 'gitops',
            'project_slug': 'microsrvc',
            'framework': 'SpringBoot',
            'files_present': [
                'microsrvc/.git/config',
                'microsrvc/.gitignore',
                'microsrvc/.dockerignore',
                'microsrvc/README.rst',
                'microsrvc/docker-compose.yml',
                'microsrvc/Dockerfile',
                'microsrvc-gitops/.git/config',
                'microsrvc-gitops/.gitignore',
                'microsrvc-gitops/deployment/application/base/kustomization.yaml',  # noqa
                'microsrvc-gitops/deployment/database/base/kustomization.yaml',
                'microsrvc-gitops/deployment/webserver/',
                'microsrvc-gitops/README.rst',
            ],
            'files_absent': [
                'microsrvc/deployment/',
                'microsrvc/gitops/',
                'microsrvc-gitops/docker-compose.yml',
                'microsrvc-gitops/Dockerfile',
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,no-self-use
    def test_gitops(self, cookies, deployment_strategy, project_slug,
                    framework, files_present, files_absent):
        """
        Generate a project with a specific deployment strategy and verify
        it is complete and working.
        """
        result = cookies.bake(extra_context={
            'deployment_strategy': deployment_strategy,
            'project_slug': project_slug,
            'framework': framework,
        })

        assert result.exit_code == 0
        assert result.exception is None

        for filename in files_present:
            thefile = result.project.join('..').join(filename)
            assert thefile.exists(), \
                'File %s missing in generated project.' % filename

        for filename in files_absent:
            thefile = result.project.join('..').join(filename)
            assert not thefile.exists(), \
                'File %s found in generated project.' % filename

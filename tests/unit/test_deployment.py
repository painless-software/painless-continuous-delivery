"""Tests for generating a deployment configuration."""
from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


# pylint: disable=too-few-public-methods
class TestDeployment:
    """
    Tests for verifying generated deployment configuration of this
    cookiecutter, executed several times with different values (test
    scenarios).
    """
    scenarios = [
        ('k8s', {}),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_deploy_config(self, cookies):
        """
        Generate a deployment configuration and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': 'myproject',
            'framework': 'Django',
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == 'myproject'
        assert result.project.isdir()
        assert result.project.join('deployment').isdir()
        
        deployment_base = \
            result.project.join('deployment', 'application', 'base')

        assert deployment_base.isdir()

        kustom_lines = \
            deployment_base.join('kustomization.yaml').readlines(cr=False)

        assert 'configMapGenerator:' in kustom_lines

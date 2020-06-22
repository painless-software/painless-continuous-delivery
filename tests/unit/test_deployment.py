"""Tests for generating a deployment configuration."""
from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


# pylint: disable=attribute-defined-outside-init,too-many-instance-attributes
class TestDeployment:
    """
    Tests for verifying generated deployment configuration of this
    cookiecutter, executed several times with different values (test
    scenarios).
    """
    scenarios = [
        ('dedicated', {
            'vcs_platform': 'GitLab.com',
            'strategy': 'dedicated',
            'cronjobs': '(none)',
            'production_domain': 'mydomain.com',
            'files_present': [],
            'files_absent': [],
        }),
        ('shared', {
            'vcs_platform': 'Bitbucket.org',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': '(automatic)',
            'files_present': [],
            'files_absent': [],
        }),
        ('no_cronjobs', {
            'vcs_platform': 'GitHub.com',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': '(automatic)',
            'files_present': [],
            'files_absent': [
                'cronjob.yaml',
                'cronjob',
            ],
        }),
        ('simple_cronjob', {
            'vcs_platform': 'GitLab.com',
            'strategy': 'shared',
            'cronjobs': 'simple',
            'production_domain': '(automatic)',
            'files_present': [
                'cronjob.yaml',
            ],
            'files_absent': [
                'cronjob',
            ],
        }),
        ('complex_cronjobs', {
            'vcs_platform': 'Bitbucket.org',
            'strategy': 'shared',
            'cronjobs': 'complex',
            'production_domain': '(automatic)',
            'files_present': [
                'cronjob',
            ],
            'files_absent': [
                'cronjob.yaml',
            ],
        }),
    ]

    # pylint: disable=too-many-arguments
    def test_deploy_config(
            self, cookies, vcs_platform, strategy, cronjobs, production_domain,
            files_present, files_absent):
        """
        Generate a deployment configuration and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': 'myproject',
            'vcs_platform': vcs_platform,
            'environment_strategy': strategy,
            'production_domain': production_domain,
            'framework': 'Django',
            'cronjobs': cronjobs,
        })

        self.vcs_platform = vcs_platform
        self.strategy = strategy
        self.production_domain = production_domain

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == 'myproject'
        assert result.project.isdir()
        assert result.project.join('deployment').isdir()

        self.verify_folders_exist(result)
        self.read_deployment_configs()
        self.compare_deployment_configs()
        self.verify_gitlab_annotations()
        self.verify_expected_content()

        for filename in files_present:
            assert self.app_base.join(filename).exists()

        for filename in files_absent:
            assert not self.app_base.join(filename).exists()

    def verify_folders_exist(self, result):
        """
        Set instance variables while checking on directories
        """
        self.app_config = result.project.join('deployment', 'application')
        self.db_config = result.project.join('deployment', 'database')
        self.app_base = self.app_config.join('base')
        self.db_base = self.db_config.join('base')

        assert self.app_base.isdir()
        assert self.db_base.isdir()

        self.app_overlays = self.app_config.join('overlays')
        self.app_development = self.app_overlays.join('development')
        self.app_integration = self.app_overlays.join('integration')
        self.app_production = self.app_overlays.join('production')

        assert self.app_overlays.isdir()
        assert self.app_development.isdir()
        assert self.app_integration.isdir()
        assert self.app_production.isdir()

        self.db_overlays = self.db_config.join('overlays')
        self.db_development = self.db_overlays.join('development')
        self.db_integration = self.db_overlays.join('integration')
        self.db_production = self.db_overlays.join('production')

        assert self.db_overlays.isdir()
        assert self.db_development.isdir()
        assert self.db_integration.isdir()
        assert self.db_production.isdir()

    def read_deployment_configs(self):
        """
        Read Kustomize configuration
        """
        self.app_base_kustomize = \
            self.app_base.join('kustomization.yaml').readlines(cr=False)
        self.app_development_kustomize = \
            self.app_development.join('kustomization.yaml').readlines(cr=False)
        self.app_integration_kustomize = \
            self.app_integration.join('kustomization.yaml').readlines(cr=False)
        self.app_production_kustomize = \
            self.app_production.join('kustomization.yaml').readlines(cr=False)

        self.db_base_kustomize = \
            self.db_base.join('kustomization.yaml').readlines(cr=False)
        self.db_development_kustomize = \
            self.db_development.join('kustomization.yaml').readlines(cr=False)
        self.db_integration_kustomize = \
            self.db_integration.join('kustomization.yaml').readlines(cr=False)
        self.db_production_kustomize = \
            self.db_production.join('kustomization.yaml').readlines(cr=False)

    def compare_deployment_configs(self):
        """
        Verify deployment configuration
        """
        assert 'configMapGenerator:' in self.app_base_kustomize
        assert 'configMapGenerator:' in self.app_development_kustomize
        assert 'configMapGenerator:' in self.app_integration_kustomize
        assert 'configMapGenerator:' in self.app_production_kustomize

        # top of kustomization setups should stay aligned
        assert self.app_base_kustomize[:3] == self.db_base_kustomize[:3]

        identical_lines = 8 if self.vcs_platform == 'GitLab.com' else 5
        assert self.app_development_kustomize[:identical_lines] == \
            self.db_development_kustomize[:identical_lines]
        assert self.app_integration_kustomize[:identical_lines] == \
            self.db_integration_kustomize[:identical_lines]
        assert self.app_production_kustomize[:identical_lines] == \
            self.db_production_kustomize[:identical_lines]

        app_base_route = self.app_base.join('route.yaml').readlines(cr=False)
        assert '  name: myproject' in app_base_route

    def verify_gitlab_annotations(self):
        """
        Make sure GitLab annotation are absent or present
        """
        should_be_present = (self.vcs_platform == 'GitLab.com')
        message = 'GitLab annotations should be %s for %s\n-------\n{}' % (
            'present' if should_be_present else 'absent',
            self.vcs_platform,
        )

        kustomize_dev = '\n'.join(self.app_development_kustomize)
        kustomize_int = '\n'.join(self.app_integration_kustomize)
        kustomize_prod = '\n'.join(self.app_production_kustomize)
        assert (
            'commonAnnotations:\n'
            '  app.gitlab.com/app: company-or-username-myproject\n'
            '  app.gitlab.com/env: development\n' in kustomize_dev
            ) is should_be_present, \
            message.format(kustomize_dev)

        assert (
            'commonAnnotations:\n'
            '  app.gitlab.com/app: company-or-username-myproject\n'
            '  app.gitlab.com/env: integration\n' in kustomize_int
            ) is should_be_present, \
            message.format(kustomize_int)

        assert (
            'commonAnnotations:\n'
            '  app.gitlab.com/app: company-or-username-myproject\n'
            '  app.gitlab.com/env: production\n' in kustomize_prod
            ) is should_be_present, \
            message.format(kustomize_prod)

    def verify_expected_content(self):
        """
        Make sure certain files contain what they should
        """
        app_prod_route_manifest = self.app_production.join('route.yaml').read()
        spec_pattern = '\nspec:\n  host: %s\n'
        custom_domain = None if self.production_domain == '(automatic)' \
            else self.production_domain

        if custom_domain:
            assert spec_pattern % custom_domain in app_prod_route_manifest, \
                "Host %s not found in Production route manifest:\n" \
                "%s" % (custom_domain, app_prod_route_manifest)
            assert '- route.yaml' in self.app_production_kustomize, \
                "route.yaml not included in Kustomize production config:\n" \
                "%s" % '\n'.join(self.app_production_kustomize)
        else:
            assert '- route.yaml' not in self.app_production_kustomize, \
                "route.yaml is included in Kustomize production config!"

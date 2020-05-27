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
        ('dedicated', {
            'strategy': 'dedicated',
            'cronjobs': '(none)',
            'files_present': [],
            'files_absent': [],
        }),
        ('shared', {
            'strategy': 'shared',
            'cronjobs': '(none)',
            'files_present': [],
            'files_absent': [],
        }),
        ('no_cronjobs', {
            'strategy': 'shared',
            'cronjobs': '(none)',
            'files_present': [],
            'files_absent': [
                'cronjob.yaml',
                'cronjob',
            ],
        }),
        ('simple_cronjob', {
            'strategy': 'shared',
            'cronjobs': 'simple',
            'files_present': [
                'cronjob.yaml',
            ],
            'files_absent': [
                'cronjob',
            ],
        }),
        ('complex_cronjobs', {
            'strategy': 'shared',
            'cronjobs': 'complex',
            'files_present': [
                'cronjob',
            ],
            'files_absent': [
                'cronjob.yaml',
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_deploy_config(
            self, cookies, strategy, cronjobs, files_present, files_absent):
        """
        Generate a deployment configuration and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': 'myproject',
            'environment_strategy': strategy,
            'framework': 'Django',
            'cronjobs': cronjobs,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == 'myproject'
        assert result.project.isdir()
        assert result.project.join('deployment').isdir()

        app_config = result.project.join('deployment', 'application')
        db_config = result.project.join('deployment', 'database')
        app_base = app_config.join('base')
        db_base = db_config.join('base')

        assert app_base.isdir()
        assert db_base.isdir()

        self.compare_deployment_configs(
            app_config, db_config, app_base, db_base, strategy)

        for filename in files_present:
            assert app_base.join(filename).exists()

        for filename in files_absent:
            assert not app_base.join(filename).exists()

    def compare_deployment_configs(
            self, app_config, db_config, app_base, db_base, strategy):
        """
        Verify deployment configuration
        """
        app_overlays = app_config.join('overlays')
        app_development = app_overlays.join('development')
        app_integration = app_overlays.join('integration')
        app_production = app_overlays.join('production')

        assert app_overlays.isdir()
        assert app_development.isdir()
        assert app_integration.isdir()
        assert app_production.isdir()

        app_base_kustomize = \
            app_base.join('kustomization.yaml').readlines(cr=False)
        app_development_kustomize = \
            app_development.join('kustomization.yaml').readlines(cr=False)
        app_integration_kustomize = \
            app_integration.join('kustomization.yaml').readlines(cr=False)
        app_production_kustomize = \
            app_production.join('kustomization.yaml').readlines(cr=False)

        assert 'configMapGenerator:' in app_base_kustomize
        assert 'configMapGenerator:' in app_development_kustomize
        assert 'configMapGenerator:' in app_integration_kustomize
        assert 'configMapGenerator:' in app_production_kustomize

        db_overlays = db_config.join('overlays')
        db_development = db_overlays.join('development')
        db_integration = db_overlays.join('integration')
        db_production = db_overlays.join('production')

        assert db_overlays.isdir()
        assert db_development.isdir()
        assert db_integration.isdir()
        assert db_production.isdir()

        db_base_kustomize = \
            db_base.join('kustomization.yaml').readlines(cr=False)
        db_development_kustomize = \
            db_development.join('kustomization.yaml').readlines(cr=False)
        db_integration_kustomize = \
            db_integration.join('kustomization.yaml').readlines(cr=False)
        db_production_kustomize = \
            db_production.join('kustomization.yaml').readlines(cr=False)

        # top of kustomization setups should stay aligned
        assert app_base_kustomize[:4] == db_base_kustomize[:4]
        if strategy == 'dedicated':
            assert app_development_kustomize[:7] == db_development_kustomize[:7]
            assert app_integration_kustomize[:6] == db_integration_kustomize[:6]
            assert app_production_kustomize[:6] == db_production_kustomize[:6]
        else:
            assert app_development_kustomize[:10] == db_development_kustomize[:10]
            assert app_integration_kustomize[:10] == db_integration_kustomize[:10]
            assert app_production_kustomize[:10] == db_production_kustomize[:10]

        # review app placeholders
        assert 'nameSuffix: -REVIEW-ID' in app_development_kustomize
        assert 'nameSuffix: -REVIEW-ID' in db_development_kustomize
        assert '  app: REVIEW-ID' in app_development_kustomize
        assert '  app: REVIEW-ID' in db_development_kustomize

        app_base_route = app_base.join('route.yaml').readlines(cr=False)
        assert '  name: myproject' in app_base_route

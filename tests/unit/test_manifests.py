"""
Tests for generating the deployment manifests.
"""
from .helpers import (  # noqa, pylint: disable=unused-import
    dedent,
    pytest_generate_tests,
)


# pylint: disable=attribute-defined-outside-init,too-many-instance-attributes
class TestManifests:
    """
    Tests for verifying generated deployment configuration of this
    cookiecutter, executed several times with different values (test
    scenarios).
    """

    scenarios = [
        ('dedicated', {
            'framework': 'Django',
            'database': 'Postgres',
            'vcs_platform': 'GitLab.com',
            'cloud_platform': 'APPUiO',
            'strategy': 'dedicated',
            'cronjobs': '(none)',
            'production_domain': 'mydomain.com',
            'files_present': [
                'application/base/kustomization.yaml',
                'application/base/route.yaml',
                'application/overlays/development/kustomization.yaml',
                'application/overlays/integration/kustomization.yaml',
                'application/overlays/production/kustomization.yaml',
                'application/overlays/production/route.yaml',
                'database/base',
                'database/overlays/development/kustomization.yaml',
                'database/overlays/integration/kustomization.yaml',
                'database/overlays/production/kustomization.yaml',
            ],
            'files_absent': [],
            'required_content': [
                ('application/overlays/production/route.yaml', [
                    dedent("""
                    spec:
                      host: mydomain.com
                    """)
                ]),
                ('application/base/route.yaml', ['  name: myproject']),
                ('application/base/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonLabels:
                      component: application
                    """)
                ]),
                ('application/overlays/development/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonAnnotations:
                      app.gitlab.com/app: company-or-username-myproject
                      app.gitlab.com/env: development
                    """),
                ]),
                ('application/overlays/integration/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonAnnotations:
                      app.gitlab.com/app: company-or-username-myproject
                      app.gitlab.com/env: integration
                    """),
                ]),
                ('application/overlays/production/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonAnnotations:
                      app.gitlab.com/app: company-or-username-myproject
                      app.gitlab.com/env: production
                    """),
                    '- route.yaml',
                ]),
            ],
            'absent_content': [],
        }),
        ('shared', {
            'framework': 'Symfony',
            'database': 'MySQL',
            'vcs_platform': 'Bitbucket.org',
            'cloud_platform': '(none)',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': '(automatic)',
            'files_present': [
                'application/base/kustomization.yaml',
                'application/overlays/development/kustomization.yaml',
                'application/overlays/integration/kustomization.yaml',
                'application/overlays/production/kustomization.yaml',
                'database/base/kustomization.yaml',
                'database/overlays/development/kustomization.yaml',
                'database/overlays/integration/kustomization.yaml',
                'database/overlays/production/kustomization.yaml',
            ],
            'files_absent': [],
            'required_content': [
                ('application/base/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonLabels:
                      component: application
                    """)
                ]),
                ('application/overlays/development/kustomization.yaml', [
                    'configMapGenerator:']),
                ('application/overlays/integration/kustomization.yaml', [
                    'configMapGenerator:']),
                ('application/overlays/production/kustomization.yaml', [
                    'configMapGenerator:']),
            ],
            'absent_content': [
                ('application/overlays/development/kustomization.yaml', [
                    'app.gitlab.com/app: company-or-username-myproject',
                    'app.gitlab.com/env: development',
                ]),
                ('application/overlays/integration/kustomization.yaml', [
                    'app.gitlab.com/app: company-or-username-myproject',
                    'app.gitlab.com/env: integration',
                ]),
                ('application/overlays/production/kustomization.yaml', [
                    'app.gitlab.com/app: company-or-username-myproject',
                    'app.gitlab.com/env: production',
                    '- route.yaml',
                ]),
            ],
        }),
        ('no_cronjobs', {
            'framework': 'Flask',
            'database': 'MySQL',
            'vcs_platform': 'GitHub.com',
            'cloud_platform': '(none)',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': '(automatic)',
            'files_present': [
                'application',
                'database',
            ],
            'files_absent': [
                'application/base/cronjob',
                'application/base/cronjob.yaml',
            ],
            'required_content': [
                ('application/base/kustomization.yaml', [
                    'configMapGenerator:',
                    dedent("""
                    commonLabels:
                      component: application
                    """)
                ]),
                ('application/overlays/development/kustomization.yaml', [
                    'configMapGenerator:']),
                ('application/overlays/integration/kustomization.yaml', [
                    'configMapGenerator:']),
                ('application/overlays/production/kustomization.yaml', [
                    'configMapGenerator:']),
            ],
            'absent_content': [],
        }),
        ('simple_cronjob', {
            'framework': 'SpringBoot',
            'database': 'MySQL',
            'vcs_platform': 'GitLab.com',
            'cloud_platform': '(none)',
            'strategy': 'shared',
            'cronjobs': 'simple',
            'production_domain': '(automatic)',
            'files_present': [
                'application/base/cronjob.yaml',
                'database',
            ],
            'files_absent': [
                'application/base/cronjob',
            ],
            'required_content': [],
            'absent_content': [],
        }),
        ('complex_cronjobs', {
            'framework': 'Flask',
            'database': 'Postgres',
            'vcs_platform': 'Bitbucket.org',
            'cloud_platform': '(none)',
            'strategy': 'shared',
            'cronjobs': 'complex',
            'production_domain': '(automatic)',
            'files_present': [
                'application/base/cronjob',
                'database',
            ],
            'files_absent': [
                'application/base/cronjob.yaml',
            ],
            'required_content': [],
            'absent_content': [],
        }),
        ('no_database', {
            'framework': 'SpringBoot',
            'database': '(none)',
            'vcs_platform': 'GitLab.com',
            'cloud_platform': '(none)',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': '(automatic)',
            'files_present': [
                'application',
            ],
            'files_absent': [
                'application/base/cronjob.yaml',
                'application/base/cronjob',
                'application/base/ingress.yaml',
                'application/overlays/development/ingress-patch.yaml',
                'application/overlays/integration/ingress-patch.yaml',
                'application/base/route.yaml',
                'application/base/route-crd.yaml',
                'application/overlays/production/route.yaml',
                'database',
            ],
            'required_content': [],
            'absent_content': [
                ('application/overlays/production/kustomization.yaml', [
                    '- ingress.yaml',
                    '- route.yaml',
                ]),
            ],
        }),
        ('APPUiO', {
            'framework': 'SpringBoot',
            'database': '(none)',
            'vcs_platform': 'GitLab.com',
            'cloud_platform': 'APPUiO',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': 'appuio.example.com',
            'files_present': [
                'application/base/route.yaml',
                'application/base/route-crd.yaml',
                'application/overlays/production/route.yaml',
                'application/overlays/development',
                'application/overlays/integration',
                'application/overlays/production',
            ],
            'files_absent': [
                'application/base/ingress.yaml',
                'application/overlays/development/ingress-patch.yaml',
                'application/overlays/integration/ingress-patch.yaml',
                'database',
            ],
            'required_content': [
                ('application/base/route.yaml', [
                    dedent("""\
                    apiVersion: v1
                    kind: Route
                    metadata:
                      name: myproject
                    spec:
                      port:
                        targetPort: http
                      tls:
                        insecureEdgeTerminationPolicy: Redirect
                        termination: edge
                      to:
                        kind: Service
                        name: application
                    """),
                ]),
                ('application/base/route-crd.yaml', [
                    dedent("""
                      metadata:
                        $ref: k8s.io/apimachinery/pkg/apis/meta/v1.ObjectMeta
                      spec:
                        $ref: github.com/appuio/route.openshift.io.v1.RouteSpec
                github.com/appuio/route.openshift.io.v1.RouteSpec:
                  Schema:
                    properties:
                      to:
                        x-kubernetes-object-ref-api-version: v1
                        x-kubernetes-object-ref-kind: Service
                    """),
                ]),
            ],
            'absent_content': [
                ('application/overlays/development/kustomization.yaml', [
                    '- path: ingress-patch.yaml',
                ]),
                ('application/overlays/integration/kustomization.yaml', [
                    '- path: ingress-patch.yaml',
                ]),
            ],
        }),
        ('Rancher', {
            'framework': 'SpringBoot',
            'database': '(none)',
            'vcs_platform': 'GitLab.com',
            'cloud_platform': 'Rancher',
            'strategy': 'shared',
            'cronjobs': '(none)',
            'production_domain': 'rancher.example.com',
            'files_present': [
                'application/base/ingress.yaml',
                'application/overlays/development/ingress-patch.yaml',
                'application/overlays/integration/ingress-patch.yaml',
                'application/overlays/development',
                'application/overlays/integration',
                'application/overlays/production',
            ],
            'files_absent': [
                'application/base/route.yaml',
                'application/base/route-crd.yaml',
                'application/overlays/production/route.yaml',
                'database',
            ],
            'required_content': [
                ('application/base/ingress.yaml', [
                    dedent("""\
                    apiVersion: networking.k8s.io/v1beta1
                    kind: Ingress
                    metadata:
                      name: myproject
                    spec:
                      tls:
                      - hosts:
                        - rancher.example.com
                        secretName: application-tls-secret
                      rules:
                      - host: rancher.example.com
                        http:
                          paths:
                          - backend:
                              serviceName: application
                              servicePort: http
                            path: /
                    """),
                ]),
                ('application/base/ingress.yaml', ['  name: myproject']),
            ],
            'absent_content': [
                ('application/overlays/production/kustomization.yaml', [
                    '- route.yaml',
                ]),
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals
    def test_deploy_config(
            self, cookies, framework, database, vcs_platform, cloud_platform,
            strategy, cronjobs, production_domain, files_present,
            files_absent, required_content, absent_content):
        """
        Generate a deployment configuration and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': 'myproject',
            'vcs_platform': vcs_platform,
            'cloud_platform': cloud_platform,
            'environment_strategy': strategy,
            'production_domain': production_domain,
            'framework': framework,
            'database': database,
            'cronjobs': cronjobs,
        })

        self.vcs_platform = vcs_platform
        self.strategy = strategy
        self.production_domain = production_domain
        self.database = database

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project_path.name == 'myproject'
        assert result.project_path.is_dir()
        self.manifests = result.project_path / 'manifests'
        assert self.manifests.is_dir()

        for filename in files_present:
            assert (self.manifests / filename).exists(), \
                f"File or folder {filename} not found in manifests."

        for filename in files_absent:
            assert not (self.manifests / filename).exists(), \
                f"File or folder {filename} in manifests should be absent."

        self.verify_app_folders_exist()

        if self.database != '(none)':
            self.ensure_db_app_stay_aligned()

        for filename, chunks in required_content:
            file_content = \
                (result.project_path / 'manifests' / filename).read_text()
            for chunk in chunks:
                assert chunk in file_content, \
                    f'Not found in generated file {filename}:\n' \
                    f'"{chunk}"\n' \
                    '-----------\n' \
                    f'{file_content}'

        for filename, chunks in absent_content:
            file_content = \
                (result.project_path / 'manifests' / filename).read_text()
            for chunk in chunks:
                assert chunk not in file_content, \
                    f'Found in file {filename}, but should not be present:\n' \
                    f'"{chunk}"\n' \
                    '-----------\n' \
                    f'{file_content}'

    def verify_app_folders_exist(self):
        """
        Set instance variables while checking on directories.
        """
        self.app_config = self.manifests / 'application'
        self.app_base = self.app_config / 'base'
        self.app_overlays = self.app_config / 'overlays'
        self.app_development = self.app_overlays / 'development'
        self.app_integration = self.app_overlays / 'integration'
        self.app_production = self.app_overlays / 'production'

        assert self.app_base.is_dir()
        assert self.app_overlays.is_dir()
        assert self.app_development.is_dir()
        assert self.app_integration.is_dir()
        assert self.app_production.is_dir()

    def verify_db_folders_exist(self):
        """
        Set instance variables while checking on directories.
        """
        self.db_config = self.manifests / 'database'
        self.db_base = self.db_config / 'base'
        self.db_overlays = self.db_config / 'overlays'
        self.db_development = self.db_overlays / 'development'
        self.db_integration = self.db_overlays / 'integration'
        self.db_production = self.db_overlays / 'production'

        assert self.db_base.is_dir()
        assert self.db_overlays.is_dir()
        assert self.db_development.is_dir()
        assert self.db_integration.is_dir()
        assert self.db_production.is_dir()

    def read_app_deployment_manifests(self):
        """
        Read Kustomize configuration.
        """
        self.verify_app_folders_exist()

        self.app_base_kustomize = \
            (self.app_base / 'kustomization.yaml').read_text().splitlines()
        self.app_development_kustomize = \
            (self.app_development / 'kustomization.yaml').read_text().splitlines()
        self.app_integration_kustomize = \
            (self.app_integration / 'kustomization.yaml').read_text().splitlines()
        self.app_production_kustomize = \
            (self.app_production / 'kustomization.yaml').read_text().splitlines()

    def read_db_deployment_manifests(self):
        """
        Read Kustomize configuration.
        """
        self.verify_db_folders_exist()

        self.db_base_kustomize = \
            (self.db_base / 'kustomization.yaml').read_text().splitlines()
        self.db_development_kustomize = \
            (self.db_development / 'kustomization.yaml').read_text().splitlines()
        self.db_integration_kustomize = \
            (self.db_integration / 'kustomization.yaml').read_text().splitlines()
        self.db_production_kustomize = \
            (self.db_production / 'kustomization.yaml').read_text().splitlines()

    def ensure_db_app_stay_aligned(self):
        """
        Ensure that the top of the kustomization setups stays aligned
        across application and database deployment manifests.
        """
        self.read_app_deployment_manifests()
        self.read_db_deployment_manifests()

        assert self.app_base_kustomize[:3] == self.db_base_kustomize[:3]

        identical_lines = 8 if self.vcs_platform == 'GitLab.com' else 5
        assert self.app_development_kustomize[:identical_lines] == \
            self.db_development_kustomize[:identical_lines]
        assert self.app_integration_kustomize[:identical_lines] == \
            self.db_integration_kustomize[:identical_lines]
        assert self.app_production_kustomize[:identical_lines] == \
            self.db_production_kustomize[:identical_lines]

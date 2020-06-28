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
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '        - tox -e py37',
                '                "Remove all related resources with > '
                '  ++ USE WITH CAUTION ++\\n"',
                '                "  oc delete all,configmap,pvc,secret'
                ' -n ${TARGET} -l app=${LABEL}"',
                '    - &cleanup-resources',
                '      seiso configmaps -l app=${LABEL} --delete &&',
                '      seiso secrets -l app=${LABEL} --delete &&',
                '      seiso image history myproject --delete &&',
                '      seiso image orphans myproject --delete',
                '  - step: &deploy-review-app',
                '  - step: &deploy-integration',
                '  - step: &deploy-production',
                '    - &define-vars',
                '    - &generate-secrets-app',
                '    - &generate-secrets-db',
                '    - &cloud-login',
                '    - &cloud-tag-image',
                '    - &cloud-set-image',
                '    - &cloud-apply-app',
                '    - &cloud-apply-db',
                '    - &cleanup-resources',
                '      - *define-vars',
                '      - *generate-secrets-app',
                '      - *generate-secrets-db',
                '      - *cloud-login',
                '      - *cloud-tag-image',
                '      - *cloud-set-image',
                '      - *cloud-apply-app',
                '      - *cloud-apply-db',
                '      - *cleanup-resources',
                '      oc tag "${SOURCE}/myproject:${BITBUCKET_COMMIT}"',
                '             "${TARGET}/myproject:${IMAGE_TAG}"',
                '      pushd deployment/application/base &&',
                '      pushd deployment/application/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      pushd deployment/database/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      popd',
                '      kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '      kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '      kustomize edit add label "app:${LABEL}" &&',
                '      kustomize build | oc apply -f - &&',
                '      SOURCE=myproject',
                '      TARGET=myproject',
                '        SUFFIX=-review-pr${BITBUCKET_PR_ID}',
                '        SUFFIX=-integration',
                '        SUFFIX=-production',
                '      - IMAGE_TAG=${BITBUCKET_COMMIT}',
                '      - IMAGE_TAG=${BITBUCKET_TAG}',
            ],
        }),
        ('bitbucket-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'bitbucket-pipelines.yml',
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'required_lines': [
                '        - tox -e py37',
                '                "Remove all related resources with > '
                '  ++ USE WITH CAUTION ++\\n"',
                '                "  oc delete all,configmap,pvc,secret'
                ' -n ${TARGET} -l app=${LABEL}"',
                '    - &cleanup-resources',
                '      seiso configmaps -l app=${LABEL} --delete &&',
                '      seiso secrets -l app=${LABEL} --delete &&',
                '      seiso image history myproject --delete &&',
                '      seiso image orphans myproject --delete',
                '  - step: &deploy-review-app',
                '  - step: &deploy-integration',
                '  - step: &deploy-production',
                '    - &define-vars',
                '    - &generate-secrets-app',
                '    - &generate-secrets-db',
                '    - &cloud-login',
                '    - &cloud-tag-image',
                '    - &cloud-set-image',
                '    - &cloud-apply-app',
                '    - &cloud-apply-db',
                '    - &cleanup-resources',
                '      - *define-vars',
                '      - *generate-secrets-app',
                '      - *generate-secrets-db',
                '      - *cloud-login',
                '      - *cloud-tag-image',
                '      - *cloud-set-image',
                '      - *cloud-apply-app',
                '      - *cloud-apply-db',
                '      - *cleanup-resources',
                '      oc tag "${SOURCE}/myproject:${BITBUCKET_COMMIT}"',
                '             "${TARGET}/myproject:${IMAGE_TAG}"',
                '      pushd deployment/application/base &&',
                '      pushd deployment/application/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      pushd deployment/database/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      popd',
                '      kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '      kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '      kustomize edit add label "app:${LABEL}" &&',
                '      kustomize build | oc apply -f - &&',
                '      SOURCE=${SOURCE:-myproject}',
                '      TARGET=${TARGET:-myproject}',
                '        SOURCE=myproject-development',
                '        TARGET=myproject-development',
                '        TARGET=myproject-integration',
                '        TARGET=myproject-production',
                '        SUFFIX=-review-pr${BITBUCKET_PR_ID}',
                '      - IMAGE_TAG=${BITBUCKET_COMMIT}',
                '      - IMAGE_TAG=${BITBUCKET_TAG}',
            ],
        }),
        ('codeship', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': 'codeship-steps.yml',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '  service: app',
            ],
        }),
        ('gitlab-shared', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '    TARGET: myproject',
                '  script: tox -e py37',
                '.deploy-vars:',
                '.generate-secrets:',
                '.deploy:',
                '  extends: .deploy-vars',
                '  extends: .generate-secrets',
                '    SUFFIX: ""',
                '    SUFFIX: -review-mr${CI_MERGE_REQUEST_IID}',
                '    SUFFIX: -integration',
                '    SUFFIX: -production',
                '    LABEL: myproject',
                '    LABEL: myproject-review-mr${CI_MERGE_REQUEST_IID}',
                '    LABEL: myproject-integration',
                '    LABEL: myproject-production',
                '    APPLICATION: application-review-mr${CI_MERGE_REQUEST_IID}',  # noqa
                '    DATABASE_HOST: postgres-review-mr${CI_MERGE_REQUEST_IID}',
                '    IMAGE_TAG: ${CI_COMMIT_SHA}',
                '    IMAGE_TAG: ${CI_COMMIT_TAG}',
                '    GIT_STRATEGY: clone',
                '    GIT_STRATEGY: none',
                '    GIT_DEPTH: 7',
                '  - seiso configmaps -l app=${LABEL} --delete',
                '  - seiso secrets -l app=${LABEL} --delete',
                '  - seiso image history myproject --delete',
                '  - seiso image orphans myproject --delete',
                '  - pushd deployment/application/base &&',
                '  - pushd deployment/application/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '  - pushd deployment/database/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '    kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '    kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '    kustomize edit add label "app:${LABEL}" &&',
                '    kustomize build | oc apply -f - &&',
                '    popd',
                'stop_review:',
                '  - oc delete all,configmap,pvc,secret -n ${TARGET} -l app=${LABEL}',  # noqa
                '    auto_stop_in: 18 hours',
            ],
        }),
        ('gitlab-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'required_lines': [
                '    TARGET: myproject-production',
                '  script: tox -e py37',
                '.deploy-vars:',
                '.generate-secrets:',
                '.deploy:',
                '  extends: .deploy-vars',
                '  extends: .generate-secrets',
                '    SUFFIX: ""',
                '    SUFFIX: -review-mr${CI_MERGE_REQUEST_IID}',
                '    LABEL: myproject',
                '    LABEL: myproject-review-mr${CI_MERGE_REQUEST_IID}',
                '    APPLICATION: application-review-mr${CI_MERGE_REQUEST_IID}',  # noqa
                '    DATABASE_HOST: postgres-review-mr${CI_MERGE_REQUEST_IID}',
                '    IMAGE_TAG: ${CI_COMMIT_SHA}',
                '    IMAGE_TAG: ${CI_COMMIT_TAG}',
                '    GIT_STRATEGY: clone',
                '    GIT_STRATEGY: none',
                '    GIT_DEPTH: 7',
                '  - oc tag "${SOURCE}/myproject:${CI_COMMIT_SHA}"',
                '           "${TARGET}/myproject:${IMAGE_TAG}"',
                '  - seiso configmaps -l app=${LABEL} --delete',
                '  - seiso secrets -l app=${LABEL} --delete',
                '  - seiso image history myproject --delete',
                '  - seiso image orphans myproject --delete',
                '  - pushd deployment/application/base &&',
                '  - pushd deployment/application/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '  - pushd deployment/database/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '    kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '    kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '    kustomize edit add label "app:${LABEL}" &&',
                '    kustomize build | oc apply -f - &&',
                '    popd',
                'stop_review:',
                '  - oc delete all,configmap,pvc,secret -n ${TARGET} -l app=${LABEL}',  # noqa
                '    auto_stop_in: 18 hours',
            ],
        }),
        ('shippable', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'shippable.yml',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '  - tox',
            ],
        }),
        ('travis', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py35,py36,py37,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                'script: tox',
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_ci_setup(self, cookies, project_slug, vcs_account, vcs_platform,
                      ci_service, checks, tests, cloud_platform,
                      environment_strategy, required_lines):
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
            'database': 'Postgres',
            'cloud_platform': cloud_platform,
            'environment_strategy': environment_strategy,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == project_slug
        assert result.project.isdir()
        assert result.project.join('README.rst').isfile()

        ci_service_conf = result.project.join(ci_service).readlines(cr=False)
        for line in required_lines:
            assert line in ci_service_conf, "Not found in CI config: " \
                "'%s'\n%s" % (line, '\n'.join(ci_service_conf))

        codeship_services = result.project.join('codeship-services.yml')
        assert (ci_service == 'codeship-steps.yml' and
                codeship_services.isfile()) or not codeship_services.exists()

        # ensure this project itself stays up-to-date with the template
        verify_file_matches_repo_root(result, ci_service,
                                      max_compare_bytes=85)

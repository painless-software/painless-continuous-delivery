"""
Tests for generating a continuous integration setup.
"""
from .helpers import (  # noqa, pylint: disable=unused-import
    pytest_generate_tests,
    verify_file_matches_repo_root,
)


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
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '        - tox -e py38',
                '                "Remove all related resources with > '
                '  ++ USE WITH CAUTION ++\\n"',
                '                "  oc delete all,configmap,pvc,rolebinding,'
                'secret -n ${TARGET} -l app=${LABEL}"',
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
                '      pushd manifests/application/base &&',
                '      pushd manifests/application/overlays/'
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
                '      DATABASE_PASSWORD=$(cat /dev/urandom '
                '| tr -dc A-Za-z0-9 | head -c16)',
                '      DATABASE_HOST=${DATABASE_HOST:-postgres${SUFFIX}}',
                '      DATABASE_NAME=myproject',
                '      DATABASE_USER=myproject',
                '        --from-literal=DJANGO_DATABASE_URL=postgres://'
                '${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}/${DATABASE_NAME}',  # noqa
                '    - &generate-secrets-db',
                '      oc get secret ${DATABASE_HOST} ||',
                '      oc create secret generic ${DATABASE_HOST}',
                '        --from-literal=POSTGRESQL_DATABASE=${DATABASE_NAME}',
                '        --from-literal=POSTGRESQL_USERNAME=${DATABASE_USER}',
                '        --from-literal=POSTGRESQL_PASSWORD=${DATABASE_PASSWORD}',  # noqa
                '    - &cloud-apply-db',
                '      pushd manifests/database/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      popd',
                '      - *generate-secrets-db',
                '      - *cloud-apply-db',
            ],
            'absent_content': [],
        }),
        ('bitbucket-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'bitbucket-pipelines.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit,kubernetes',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'required_lines': [
                '        - tox -e py38',
                '                "Remove all related resources with > '
                '  ++ USE WITH CAUTION ++\\n"',
                '                "  oc delete all,configmap,pvc,rolebinding,'
                'secret -n ${TARGET} -l app=${LABEL}"',
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
                '      pushd manifests/application/base &&',
                '      pushd manifests/application/overlays/'
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
                '      DATABASE_PASSWORD=$(cat /dev/urandom '
                '| tr -dc A-Za-z0-9 | head -c16)',
                '      DATABASE_HOST=${DATABASE_HOST:-postgres${SUFFIX}}',
                '      DATABASE_NAME=myproject',
                '      DATABASE_USER=myproject',
                '        --from-literal=DJANGO_DATABASE_URL=postgres://'
                '${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}/${DATABASE_NAME}',  # noqa
                '    - &generate-secrets-db',
                '      oc get secret ${DATABASE_HOST} ||',
                '      oc create secret generic ${DATABASE_HOST}',
                '        --from-literal=POSTGRESQL_DATABASE=${DATABASE_NAME}',
                '        --from-literal=POSTGRESQL_USERNAME=${DATABASE_USER}',
                '        --from-literal=POSTGRESQL_PASSWORD=${DATABASE_PASSWORD}',  # noqa
                '    - &cloud-apply-db',
                '      pushd manifests/database/overlays/'
                '${BITBUCKET_DEPLOYMENT_ENVIRONMENT} &&',
                '      - *generate-secrets-db',
                '      - *cloud-apply-db',
            ],
            'absent_content': [],
        }),
        ('bitbucket-no-db', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'bitbucket-pipelines.yml',
            'framework': 'Flask',
            'database': '(none)',
            'checks': 'kubernetes',
            'tests': 'py38,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [],
            'absent_content': [
                'DATABASE_',
                'generate-secrets-db',
                'cloud-apply-db',
                'database',
            ],
        }),
        ('codeship', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': 'codeship-steps.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '  service: app',
            ],
            'absent_content': [],
        }),
        ('gitlab-shared', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '    TARGET: myproject',
                '  script: tox -e py38',
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
                '    IMAGE_TAG: ${CI_COMMIT_SHA}',
                '    IMAGE_TAG: ${CI_COMMIT_TAG}',
                '    GIT_STRATEGY: clone',
                '    GIT_STRATEGY: none',
                '    GIT_DEPTH: 7',
                '  - seiso configmaps -l app=${LABEL} --delete',
                '  - seiso secrets -l app=${LABEL} --delete',
                '  - seiso image history myproject --delete',
                '  - seiso image orphans myproject --delete',
                '  - pushd manifests/application/base &&',
                '  - pushd manifests/application/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '  - pushd manifests/database/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '    kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '    kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '    kustomize edit add label "app:${LABEL}" &&',
                '    kustomize build | oc apply -f - &&',
                '    popd',
                'stop_review:',
                '  - oc delete all,configmap,pvc,rolebinding,secret -n '
                '${TARGET} -l app=${LABEL}',
                '    auto_stop_in: 12 hours',
                '    DATABASE_HOST: postgres-${CI_ENVIRONMENT_NAME}',
                '    DATABASE_HOST: postgres-review-mr${CI_MERGE_REQUEST_IID}',
                '    DATABASE_NAME: myproject',
                '    DATABASE_USER: myproject',
                '  - export DATABASE_PASSWORD=$(cat /dev/urandom '
                '| tr -dc A-Za-z0-9 | head -c16)',
                '      --from-literal=DJANGO_DATABASE_URL=postgres://'
                '${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}/${DATABASE_NAME}',  # noqa
                '  - oc get secret ${DATABASE_HOST} ||',
                '    oc create secret generic ${DATABASE_HOST}',
                '      --from-literal=POSTGRESQL_DATABASE=${DATABASE_NAME}',
                '      --from-literal=POSTGRESQL_USERNAME=${DATABASE_USER}',
                '      --from-literal=POSTGRESQL_PASSWORD=${DATABASE_PASSWORD}',  # noqa
                '  - pushd manifests/database/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
            ],
            'absent_content': [],
        }),
        ('gitlab-dedicated', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'dedicated',
            'required_lines': [
                '    TARGET: myproject-production',
                '  script: tox -e py38',
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
                '  - pushd manifests/application/base &&',
                '  - pushd manifests/application/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
                '    kustomize edit set image IMAGE="docker-registry.'
                'default.svc:5000/${TARGET}/myproject:${IMAGE_TAG}" &&',
                '    kustomize edit set namesuffix -- "${SUFFIX}" &&',
                '    kustomize edit add label "app:${LABEL}" &&',
                '    kustomize build | oc apply -f - &&',
                '    popd',
                'stop_review:',
                '  - oc delete all,configmap,pvc,rolebinding,secret -n '
                '${TARGET} -l app=${LABEL}',
                '    auto_stop_in: 12 hours',
                '    DATABASE_HOST: postgres',
                '    DATABASE_HOST: postgres-review-mr${CI_MERGE_REQUEST_IID}',
                '    DATABASE_NAME: myproject',
                '    DATABASE_USER: myproject',
                '  - export DATABASE_PASSWORD=$(cat /dev/urandom '
                '| tr -dc A-Za-z0-9 | head -c16)',
                '      --from-literal=DJANGO_DATABASE_URL=postgres://'
                '${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}/${DATABASE_NAME}',  # noqa
                '  - oc get secret ${DATABASE_HOST} ||',
                '    oc create secret generic ${DATABASE_HOST}',
                '      --from-literal=POSTGRESQL_DATABASE=${DATABASE_NAME}',
                '      --from-literal=POSTGRESQL_USERNAME=${DATABASE_USER}',
                '      --from-literal=POSTGRESQL_PASSWORD=${DATABASE_PASSWORD}',  # noqa
                '  - pushd manifests/database/overlays/${CI_ENVIRONMENT_NAME} &&',  # noqa
            ],
            'absent_content': [],
        }),
        ('gitlab-no-db', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
            'framework': 'Flask',
            'database': '(none)',
            'checks': 'kubernetes',
            'tests': 'py38,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [],
            'absent_content': [
                'DATABASE_',
                'database',
            ],
        }),
        ('shippable', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'Bitbucket.org',
            'ci_service': 'shippable.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                '  - tox',
            ],
            'absent_content': [],
        }),
        ('travis', {
            'project_slug': 'myproject',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Django',
            'database': 'Postgres',
            'checks': 'flake8,pylint,bandit',
            'tests': 'py38,pypy3,behave',
            'cloud_platform': 'APPUiO',
            'environment_strategy': 'shared',
            'required_lines': [
                'script: tox',
            ],
            'absent_content': [],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_ci_setup(self, cookies, project_slug, vcs_account, vcs_platform,
                      ci_service, framework, database, checks, tests,
                      cloud_platform, environment_strategy, required_lines,
                      absent_content):
        """
        Generate a CI setup with specific settings and verify it is complete.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'framework': framework,
            'database': database,
            'checks': checks,
            'tests': tests,
            'cloud_platform': cloud_platform,
            'environment_strategy': environment_strategy,
        })

        assert result.exit_code == 0
        assert result.exception is None

        assert result.project.basename == project_slug
        assert result.project.isdir()
        readme_file = result.project.join('README.rst')
        assert readme_file.isfile()

        readme_content = '\n'.join(readme_file.readlines(cr=False))
        assert '\n\n\n' not in readme_content, \
            f"Excessive newlines in README: {readme_file}\n" \
            f"-------------\n{readme_content}"

        ci_service_conf = result.project.join(ci_service).readlines(cr=False)
        ci_service_content = '\n'.join(ci_service_conf)
        assert '\n\n\n' not in ci_service_content, \
            "Excessive newlines in CI configuration."

        for line in required_lines:
            assert line in ci_service_conf, \
                f"Not found in CI config: '{line}'\n" \
                f"{ci_service_content}"

        for chunk in absent_content:
            assert chunk not in ci_service_content, \
                f"Found in CI config: '{chunk}'\n" \
                f"{ci_service_content}"

        codeship_services = result.project.join('codeship-services.yml')
        assert (ci_service == 'codeship-steps.yml' and
                codeship_services.isfile()) or not codeship_services.exists()

        files_absent = ['gitops', f"../{project_slug}-gitops"]
        for filename in files_absent:
            thefile = result.project.join(filename)
            assert not thefile.exists(), \
                f'File {filename} found in generated project.'

        # ensure this project itself stays up-to-date with the template
        verify_file_matches_repo_root(result, ci_service,
                                      max_compare_bytes=85)

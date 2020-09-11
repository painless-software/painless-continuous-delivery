"""
Tests for the GitOps deployment strategy.
"""
from .helpers import (  # noqa, pylint: disable=unused-import
    dedent,
    indent2,
    pytest_generate_tests,
)


# pylint: disable=too-few-public-methods
class TestGitops:
    """
    Tests for verifying generated projects deployed using GitOps.
    """
    scenarios = [
        ('Bitbucket', {
            'project_slug': 'bitbucket',
            'framework': 'SpringBoot',
            'ci_service': 'bitbucket-pipelines.yml',
            'cloud_platform': 'APPUiO',
            'docker_registry': "registry.appuio.ch",
            'files_present': [
                'bitbucket/.git/config',
                'bitbucket/.gitignore',
                'bitbucket/.dockerignore',
                'bitbucket/bitbucket-pipelines.yml',
                'bitbucket/README.rst',
                'bitbucket/docker-compose.yml',
                'bitbucket/Dockerfile',
                'bitbucket-gitops/.git/config',
                'bitbucket-gitops/.gitignore',
                'bitbucket-gitops/bitbucket-pipelines.yml',
                'bitbucket-gitops/application/base/kustomization.yaml',
                'bitbucket-gitops/bootstrap.sh',
                'bitbucket-gitops/README.rst',
            ],
            'files_absent': [
                'bitbucket/gitops/',
                'bitbucket-gitops/_/',
                'bitbucket-gitops/database/',
                'bitbucket-gitops/docker-compose.yml',
                'bitbucket-gitops/Dockerfile',
            ],
            'required_content': [
                ('bitbucket/bitbucket-pipelines.yml', [
                    indent2("""
                    - step: &build
                        name: Build image
                        image: docker.io/library/docker:19.03.8
                        caches:
                        - docker
                        script:
                        - REGISTRY=registry.appuio.ch
                          TARGET=bitbucket
                          IMAGE="${REGISTRY}/${TARGET}/bitbucket"
                        - *docker-login
                        - *build-image
                        - *push-image
                    """),
                    indent2("""
                    - step: &tag-review-app-image
                        name: Tag review app image
                        deployment: development
                        image: docker.io/library/docker:19.03.8
                        caches:
                        - docker
                        script:
                        - IMAGE_TAG=review-pr${BITBUCKET_PR_ID}
                        - *define-vars
                        - *docker-login
                        - *tag-image
                        - *push-image
                    """),
                    indent2("""
                    - step: &tag-integration-image
                        name: Tag integration image
                        deployment: integration
                        image: docker.io/library/docker:19.03.8
                        caches:
                        - docker
                        script:
                        - IMAGE_TAG=latest
                        - *define-vars
                        - *docker-login
                        - *tag-image
                        - *push-image
                    """),
                    indent2("""
                    - step: &tag-production-image
                        name: Tag production image
                        deployment: production
                        image: docker.io/library/docker:19.03.8
                        script:
                        - IMAGE_TAG=${BITBUCKET_TAG}
                        - *define-vars
                        - *docker-login
                        - *tag-image
                        - *push-image
                    """),
                    dedent("""
                    pipelines:
                      pull-requests:
                        '**':
                        - parallel: *checks
                        - parallel: *tests
                        - step: *build
                        - step: *tag-review-app-image
                    """),
                    indent2("""
                      branches:
                        master:
                        - parallel: *checks
                        - parallel: *tests
                        - step: *build
                        - step: *tag-integration-image
                    """),
                    indent2("""
                      tags:
                        '*':
                        - step: *tag-production-image
                    """),
                ]),
                ('bitbucket-gitops/bitbucket-pipelines.yml', [
                    dedent("""
                definitions:
                  steps:
                  - parallel: &checks
                    - step:
                        name: Lint manifests
                        image: docker.io/garethr/kubeval:latest
                        script:
                        - /kubeval --strict --ignore-missing-schemas **/*.yaml
                    """),
                    dedent("""
                    pipelines:
                      default:
                      - parallel: *checks
                    """),
                ]),
                ('bitbucket-gitops/application/overlays/development/'
                    'kustomization.yaml', [
                        dedent("""
                    images:
                    - name: IMAGE
                      newName: registry.appuio.ch/bitbucket/bitbucket:latest
                    """),
                ]),  # noqa
            ],
        }),
        ('Codeship', {
            'project_slug': 'codeship',
            'framework': 'SpringBoot',
            'ci_service': 'codeship-steps.yml',
            'cloud_platform': 'Rancher',
            'docker_registry': "registry.rancher.example",
            'files_present': [
                'codeship/.git/config',
                'codeship/.gitignore',
                'codeship/.dockerignore',
                'codeship/codeship-services.yml',
                'codeship/codeship-steps.yml',
                'codeship/README.rst',
                'codeship/docker-compose.yml',
                'codeship/Dockerfile',
                'codeship-gitops/.git/config',
                'codeship-gitops/.gitignore',
                'codeship-gitops/codeship-services.yml',
                'codeship-gitops/codeship-steps.yml',
                'codeship-gitops/application/base/kustomization.yaml',
                'codeship-gitops/bootstrap.sh',
                'codeship-gitops/README.rst',
            ],
            'files_absent': [
                'codeship/gitops/',
                'codeship-gitops/_/',
                'codeship-gitops/database/',
                'codeship-gitops/docker-compose.yml',
                'codeship-gitops/Dockerfile',
            ],
            'required_content': [
                ('codeship-gitops/codeship-steps.yml', [
                    dedent("""
            - name: Checks
              type: parallel
              service: app
              steps:
              - name: Lint manifests
                command: /kubeval --strict --ignore-missing-schemas **/*.yaml
                    """),
                ]),
                ('codeship-gitops/application/overlays/development/'
                    'kustomization.yaml', [
                        dedent("""
                images:
                - name: IMAGE
                  newName: registry.rancher.example/codeship/codeship:latest
                """),
                ]),  # noqa
            ],
        }),
        ('GitLab', {
            'project_slug': 'gitlab',
            'framework': 'SpringBoot',
            'ci_service': '.gitlab-ci.yml',
            'cloud_platform': 'Rancher',
            'docker_registry': "registry.rancher.example",
            'files_present': [
                'gitlab/.git/config',
                'gitlab/.gitignore',
                'gitlab/.dockerignore',
                'gitlab/.gitlab-ci.yml',
                'gitlab/README.rst',
                'gitlab/docker-compose.yml',
                'gitlab/Dockerfile',
                'gitlab-gitops/.git/config',
                'gitlab-gitops/.gitignore',
                'gitlab-gitops/.gitlab-ci.yml',
                'gitlab-gitops/application/base/kustomization.yaml',
                'gitlab-gitops/bootstrap.sh',
                'gitlab-gitops/README.rst',
            ],
            'files_absent': [
                'gitlab/gitops/',
                'gitlab-gitops/_/',
                'gitlab-gitops/database/',
                'gitlab-gitops/docker-compose.yml',
                'gitlab-gitops/Dockerfile',
            ],
            'required_content': [
                ('gitlab/.gitlab-ci.yml', [
                    dedent("""
                    app-image:
                      extends: .build
                      environment:
                        name: development
                      only:
                      - merge_requests
                      - master
                    """),
                    dedent("""
                    review:
                      extends: .tag-image
                      environment:
                        name: development
                      variables:
                        IMAGE_TAG: review-mr${CI_MERGE_REQUEST_IID}
                      only:
                      - merge_requests
                    """),
                    dedent("""
                    integration:
                      extends: .tag-image
                      environment:
                        name: integration
                      variables:
                        IMAGE_TAG: latest
                      only:
                      - master
                    """),
                    dedent("""
                    production:
                      extends: .tag-image
                      environment:
                        name: production
                      variables:
                        IMAGE_TAG: "${CI_COMMIT_TAG}"
                      only:
                      - tags
                    """),
                ]),
                ('gitlab-gitops/.gitlab-ci.yml', [
                    dedent("""
                    stages:
                    - lint

                    lint:
                      stage: lint
                      image:
                        name: docker.io/garethr/kubeval:latest
                        entrypoint: [""]
                      script:
                      - /kubeval --strict --ignore-missing-schemas **/*.yaml
                    """),
                ]),
                ('gitlab-gitops/application/overlays/development/'
                    'kustomization.yaml', [
                        dedent("""
                    images:
                    - name: IMAGE
                      newName: registry.rancher.example/gitlab/gitlab:latest
                    """),
                ]),  # noqa
            ],
        }),
    ]

    # pylint: disable=no-self-use,too-many-arguments,too-many-locals
    def test_gitops(self, cookies, project_slug, framework, ci_service,
                    cloud_platform, docker_registry, files_present,
                    files_absent, required_content):
        """
        Generate a project with a specific deployment strategy and verify
        it is complete and working.
        """
        result = cookies.bake(extra_context={
            'deployment_strategy': 'gitops',
            'project_slug': project_slug,
            'framework': framework,
            'ci_service': ci_service,
            'cloud_platform': cloud_platform,
            'docker_registry': docker_registry,
        })

        assert result.exit_code == 0
        assert result.exception is None

        for filename in files_present:
            thefile = result.project.join("..", filename)
            assert thefile.exists(), \
                'File %s missing in generated project.' % filename

        for filename in files_absent:
            thefile = result.project.join('..').join(filename)
            assert not thefile.exists(), \
                'File %s found in generated project.' % filename

        app_readme_file = result.project.join("README.rst")
        gitops_readme_file = result.project.join(
            "..", f"{project_slug}-gitops", "README.rst")

        for readme_file in [app_readme_file, gitops_readme_file]:
            assert readme_file.isfile()
            readme_content = '\n'.join(gitops_readme_file.readlines(cr=False))
            assert '\n\n\n' not in readme_content, \
                f"Excessive newlines in README: {readme_file}\n" \
                f"-------------\n{readme_content}"

        ci_service_conf = result.project.join(ci_service).readlines(cr=False)
        assert '\n\n\n' not in '\n'.join(ci_service_conf), \
            "Excessive newlines in micro-service CI config."

        gitops_ci_conf = result.project.join(
            "..", f"{project_slug}-gitops", ci_service).readlines(cr=False)
        assert '\n\n\n' not in '\n'.join(gitops_ci_conf), \
            "Excessive newlines in GitOps CI config."

        for filename, chunks in required_content:
            file_content = result.project.join("..", filename).read()
            for chunk in chunks:
                assert chunk in file_content, \
                    'Not found in generated file %s:\n"%s"\n' \
                    '-----------\n%s' % \
                    (filename, chunk, file_content)

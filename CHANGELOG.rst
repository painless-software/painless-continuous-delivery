Change Log
==========

All notable changes to this project are documented in this file.

0.8.0 (unreleased)
------------------

- Use ruff for linting (instead of Flake8, isort, Pylint, etc.)
- Drop CI support for Codeship
- Drop Python 3.8
- Drop direnv support (.envrc configuration file)
- Drop PHP project support (Symfony and TYPO3 Web frameworks)

0.7.0 (2022-02-19)
------------------

- Drop Shippable and Travis CI (ceased public service after being acquired)
- Rename deployment/ folder to manifests/ to match Kubernetes realities
- Introduce pyproject.toml for tool configuration
- Drop Python 3.6 and 3.7 from Tox configurations and CI
- Upgrade Django to 3.2 LTS and 4.0 (both use pathlib in settings)
- Migrate Python setup to 3.8 on Alpine (from 3.7 on Debian)

0.6.0 (2021-01-08)
------------------

- Rename whitelist to allowlist in Tox configuration (Black Lives Matter)
- Deploy more field tests (Flask/Bitbucket, Spring+GitOps)
- Restructure directory layout to accommodate GitOps (generation of two repos)
- Use pathlib in unit tests more consistently
- Refactor code in tests.unit into tests.unit.helpers (keep ``__init__`` clean)
- Add Java Spring Framework project skeleton
- Add Python 3.8, drop Python 3.5 from CI jobs
- Rename database option 'MySQL/MariaDB' to just 'MySQL'

0.5.0 (2020-02-07)
------------------

- Add cron jobs with Kubernetes manifests (simple, complex)
- Enable environment variables via Kubernetes ConfigMap object
- Manage cluster permissions via Kubernetes RoleBinding objects
- Enable GitLab integration with target cluster
- Use Kustomize for deployments (instead of OpenShift templates)
- Allow a shared namespace (alternative to 3 dedicated namespaces)
- Automatically deploy a field test on each change

0.4.0 (2019-06-21)
------------------

- Prepare New Relic integration for Django
- Update Sentry integration for Django
- Add Django debug toolbar setup
- Remove Vexor (discontinued CI service)
- Add Python security scanner (Bandit) and PyClean
- Generate deployment configuration for APPUiO (OpenShift)
- Add running Python doctests
- Run parallel build jobs on Bitbucket Pipelines and Codeship
- Use stages on Travis CI

0.3.0 (2017-07-24)
------------------

- Make GitLab CI configuration more readable
- Add Python 3.6, drop Python 3.3 (CI server issues)
- Add Symfony, TYPO3 project skeletons
- Add new options: docker_registry, checks
- Add functional tests for Django, Flask, Symfony
- Add experimental direnv support (.envrc configuration file)
- Add Docker Compose v3 override configuration (PHP frameworks)

0.2.0 (2017-03-28)
------------------

- Generalize deployment (allow adding other technologies)
- Add 'PHP generic' as a framework option

0.1.0 (2017-02-02)
------------------

- Generate Tox test setup supporting pytest, flake8, pylint, behave
- Generate CI configuration for Bitbucket Pipelines, Codeship, GitLab CI,
  Shippable, Travis CI, Vexor
- Generate project skeletons for Django, Flask
- Generate Docker Compose setup for local development
- Support uWSGI and Nginx for deployment
- Support Postgres and MySQL/MariaDB databases
- Support generation of common licenses
- Set Git remote for GitHub, GitLab, Bitbucket
- Add Landscape badge to README for monitoring software health of this project
- Support Sentry for application monitoring and crash reporting

Change Log
==========

All notable changes to this project are documented in this file.
This project adheres to `Semantic Versioning <https://semver.org>`__.

0.7.0 (unreleased)
------------------

- Migrate Python setup to 3.8 on Alpine (from 3.7 on Debian)

0.6.0 (2021-01-08)
------------------

- Rename whitelist to allowlist in Tox configuration (Black Lives Matter)
- Deploy more field tests (Flask/Bitbucket, Spring+GitOps)
- Restructure directory layout to accomodate GitOps (generation of two repos)
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

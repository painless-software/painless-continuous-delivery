Change Log
==========

All notable changes to this project are documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

0.4.0 (2019-MM-DD)
------------------

- Generate Kubernetes/OpenShift deployment configuration
- Remove Vexor (discontinued CI service)

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
- Support Posgres and MariaDB/MySQL databases
- Support generation of common licenses
- Set Git remote for GitHub, GitLab, Bitbucket
- Add Landscape badge to README for monitoring software health of this project
- Support Sentry for application monitoring and crash reporting

"""Tests for generating a Web framework project."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


# pylint: disable=too-few-public-methods
class TestFramework:
    """
    Tests for verifying generated projects using specific Web frameworks.
    """
    scenarios = [
        ('django', {
            'project_slug': 'django-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Django',
            'checks': 'flake8,pylint',
            'tests': 'py35,py36,py37,pypy3,behave',
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.in',
                'requirements.txt',
                'requirements-dev.txt',
                'manage.py',
                'application/wsgi.py',
                'deployment/application/Dockerfile',
                'deployment/application/entrypoint.sh',
                'deployment/application/uwsgi.ini',
                'deployment/webserver/nginx.conf',
                'tox.ini',
                'tests/README.rst',
            ],
            'required_content': [
                ('deployment/application/Dockerfile', [
                    'ARG REQUIREMENTS=requirements.txt',
                    'COPY requirements* ./',
                ]),
                ('docker-compose.yml', [
                    '    environment:',
                    '      - DJANGO_DEBUG=True',
                    '    command: '
                    '["python", "manage.py", "runserver", "0.0.0.0:8000"]',
                    '    ports:',
                    '      - "8000:8000"',
                ]),
            ],
            'install_commands': [
                ('pip install -r %s', 'requirements.txt'),
            ],
        }),
        ('flask', {
            'project_slug': 'flask-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Flask',
            'checks': 'flake8,pylint',
            'tests': 'py35,py36,py37,pypy3,behave',
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.in',
                'requirements.txt',
                'requirements-dev.txt',
                'application/wsgi.py',
                'deployment/application/Dockerfile',
                'deployment/application/entrypoint.sh',
                'deployment/application/uwsgi.ini',
                'deployment/webserver/nginx.conf',
                'tox.ini',
                'tests/README.rst',
            ],
            'required_content': [
                ('deployment/application/Dockerfile', [
                    'ARG REQUIREMENTS=requirements.txt',
                    'COPY requirements* ./',
                ]),
                ('docker-compose.yml', [
                    '    environment:',
                    '      - FLASK_APP=application',
                    '      - FLASK_ENV=development',
                    '    command: ["flask", "run", "--host", "0.0.0.0"]',
                    '    ports:',
                    '      - "5000:5000"',
                ]),
            ],
            'install_commands': [
                ('pip install -r %s', 'requirements.txt'),
            ],
        }),
        ('symfony', {
            'project_slug': 'symfony-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Symfony',
            'checks': 'phpcs,twig',
            'tests': 'phpunit',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'deployment/application/Dockerfile',
                'deployment/application/php.ini',
                'deployment/webserver/000-default.conf',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'src/.htaccess',
                'src/AppBundle/AppBundle.php',
                'web/.htaccess',
                'web/app.php',
            ],
            'required_content': [
            ],
            'install_commands': [
            ],
        }),
        ('typo3', {
            'project_slug': 'typo3-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'TYPO3',
            'checks': 'phpcs',
            'tests': 'phpunit',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'deployment/application/Dockerfile',
                'deployment/application/php.ini',
                'deployment/webserver/000-default.conf',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'web/typo3conf/ext/typo3_console/ext_emconf.php',
                'web/typo3conf/ext/typo3_console/ext_icon.png',
            ],
            'required_content': [
            ],
            'install_commands': [
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_framework(self, cookies, project_slug, vcs_account, vcs_platform,
                       ci_service, framework, checks, tests, required_files,
                       required_content, install_commands):
        """
        Generate a framework project and verify it is complete and working.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'framework': framework,
            'checks': checks,
            'tests': tests,
        })

        assert result.exit_code == 0
        assert result.exception is None

        for filename in required_files:
            thefile = result.project.join(filename)
            assert thefile.isfile(), \
                'File %s missing in generated project.' % filename

        for filename, required_lines in required_content:
            file_content = result.project.join(filename).readlines(cr=False)
            for line in required_lines:
                assert line in file_content, \
                    'Line not found in generated file %s: "%s"' % \
                    (filename, line)

        for cmd_pattern, project_file in install_commands:
            input_file = result.project.join(project_file)
            command = cmd_pattern % input_file
            assert input_file.isfile()
            exit_code = system(command)
            assert exit_code == 0, 'Command fails: %s' % command

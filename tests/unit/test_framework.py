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
            'framework': 'Django',
            'checks': 'flake8,pylint',
            'tests': 'py36,py37,py38,pypy3,behave',
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.in',
                'requirements.txt',
                'requirements-dev.txt',
                'manage.py',
                'application/wsgi.py',
                'Dockerfile',
                'entrypoint.sh',
                'deployment/nginx.conf',
                'deployment/uwsgi.ini',
                'tox.ini',
                'tests/README.rst',
            ],
            'required_content': [
                ('Dockerfile', [
                    'ARG REQUIREMENTS=requirements.txt',
                    'COPY requirements* ./',
                    'CMD ["uwsgi", "deployment/uwsgi.ini"]',
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
            'framework': 'Flask',
            'checks': 'flake8,pylint',
            'tests': 'py36,py37,py38,pypy3,behave',
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.in',
                'requirements.txt',
                'requirements-dev.txt',
                'application/wsgi.py',
                'Dockerfile',
                'entrypoint.sh',
                'deployment/nginx.conf',
                'deployment/uwsgi.ini',
                'tox.ini',
                'tests/README.rst',
            ],
            'required_content': [
                ('Dockerfile', [
                    'ARG REQUIREMENTS=requirements.txt',
                    'COPY requirements* ./',
                    'CMD ["uwsgi", "deployment/uwsgi.ini"]',
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
        ('springboot', {
            'project_slug': 'springboot-project',
            'framework': 'SpringBoot',
            'checks': 'lint',
            'tests': 'test',
            'required_files': [
                '.envrc',
                '.gitignore',
                'build.gradle',
                'Dockerfile',
                'docker-compose.yml',
                'gradle.properties',
                'gradlew',
                'gradlew.bat',
                'mvnw',
                'mvnw.cmd',
                'pom.xml',
                'settings.gradle',
                '.mvn/wrapper/maven-wrapper.jar',
                '.mvn/wrapper/maven-wrapper.properties',
                '.mvn/wrapper/MavenWrapperDownloader.java',
                'gradle/wrapper/gradle-wrapper.jar',
                'gradle/wrapper/gradle-wrapper.properties',
                'src/main/java/hello/Application.java',
                'src/main/resources/application.yml',
            ],
            'required_content': [
                ('Dockerfile', [
                    'FROM openjdk:8-jdk-alpine',
                    'COPY . .',
                ]),
                ('docker-compose.yml', [
                    '      dockerfile: Dockerfile',
                    '    ports:',
                    '      - "8080:8080"',
                ]),
            ],
            'install_commands': [
            ],
        }),
        ('symfony', {
            'project_slug': 'symfony-project',
            'framework': 'Symfony',
            'checks': 'phpcs,twig',
            'tests': 'phpunit',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'Dockerfile',
                'deployment/000-default.conf',
                'deployment/php.ini',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'src/.htaccess',
                'src/AppBundle/AppBundle.php',
                'web/.htaccess',
                'web/app.php',
            ],
            'required_content': [
                ('Dockerfile', [
                    'FROM php:7.0-apache',
                    ' && mv deployment/php.ini /usr/local/etc/php/ \\',
                ]),
            ],
            'install_commands': [
            ],
        }),
        ('typo3', {
            'project_slug': 'typo3-project',
            'framework': 'TYPO3',
            'checks': 'phpcs',
            'tests': 'phpunit',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'Dockerfile',
                'deployment/000-default.conf',
                'deployment/php.ini',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'web/typo3conf/ext/typo3_console/ext_emconf.php',
                'web/typo3conf/ext/typo3_console/ext_icon.png',
            ],
            'required_content': [
                ('Dockerfile', [
                    'FROM php:7.0-apache',
                    ' && mv deployment/php.ini /usr/local/etc/php/ \\',
                ]),
            ],
            'install_commands': [
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_framework(self, cookies, project_slug, framework, checks, tests,
                       required_files, required_content, install_commands):
        """
        Generate a framework project and verify it is complete and working.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
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

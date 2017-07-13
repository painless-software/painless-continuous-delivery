"""Tests for generating a Web framework project."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import
from . import verify_file_matches_repo_root


# pylint: disable=too-few-public-methods
class TestFramework(object):
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
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.txt',
                'manage.py',
                'application/wsgi.py',
                'config/application/Dockerfile',
                'config/application/uwsgi.ini',
                'config/webserver/Dockerfile',
                'config/webserver/nginx.conf',
                'tox.ini',
                'tests/README.rst',
                'tests/requirements.txt',
            ],
            'install_commands': [
                ('pip install -r %s', 'requirements.txt'),
            ],
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:pylint]',
                ]),
            ],
            'checks': 'flake8,pylint',
            'tests': 'py27,py34,py35,py36,pypy,behave',
        }),
        ('flask', {
            'project_slug': 'flask-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Flask',
            'required_files': [
                '.envrc',
                '.gitignore',
                'requirements.txt',
                'runserver.py',
                'application/wsgi.py',
                'config/application/Dockerfile',
                'config/application/uwsgi.ini',
                'config/webserver/Dockerfile',
                'config/webserver/nginx.conf',
                'tox.ini',
                'tests/README.rst',
                'tests/requirements.txt',
            ],
            'install_commands': [
                ('pip install -r %s', 'requirements.txt'),
            ],
            'test_configuration': [
                ('tox.ini', [
                    '[tox]',
                    '[testenv]',
                    '[testenv:flake8]',
                    '[testenv:pylint]',
                ]),
            ],
            'checks': 'flake8,pylint',
            'tests': 'py27,py34,py35,py36,pypy,behave',
        }),
        ('symfony', {
            'project_slug': 'symfony-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'Symfony',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'config/webserver/Dockerfile',
                'config/webserver/php.ini',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'src/.htaccess',
                'src/AppBundle/AppBundle.php',
                'web/.htaccess',
                'web/app.php',
            ],
            'install_commands': [
            ],
            'test_configuration': [
                ('composer.json', [
                    '        "check": [\n'
                    '            "@composer phpcs",\n'
                    '            "@composer twig"\n'
                    '        ],',
                    '        "test": [\n'
                    '            "@composer phpunit"\n'
                    '        ],',
                ]),
            ],
            'checks': 'phpcs,twig',
            'tests': 'phpunit',
        }),
        ('typo3', {
            'project_slug': 'typo3-project',
            'vcs_account': 'painless-software',
            'vcs_platform': 'GitHub.com',
            'ci_service': '.travis.yml',
            'framework': 'TYPO3',
            'required_files': [
                '.envrc',
                '.gitignore',
                'composer.json',
                'composer.lock',
                'config/webserver/Dockerfile',
                'config/webserver/php.ini',
                'docker-compose.yml',
                'docker-compose.override.yml',
                'docker-compose.final.yml',
                'web/typo3conf/ext/typo3_console/ext_emconf.php',
                'web/typo3conf/ext/typo3_console/ext_icon.png',
            ],
            'install_commands': [
            ],
            'test_configuration': [
                ('composer.json', [
                ]),
            ],
            'checks': 'phpcs',
            'tests': 'phpunit',
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_framework(self, cookies, project_slug, vcs_account, vcs_platform,
                       ci_service, framework, required_files,
                       install_commands, test_configuration, checks, tests):
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

        for cmd_pattern, project_file in install_commands:
            input_file = result.project.join(project_file)
            command = cmd_pattern % input_file
            assert input_file.isfile()
            exit_code = system(command)
            assert exit_code == 0, 'Command fails: %s' % command

        for filename, expected_content in test_configuration:
            config_file = result.project.join(filename).read()
            for config_value in expected_content:
                assert config_value in config_file, \
                    'Configuration value missing in {filename}: {value}\n' \
                    '--------------- (content follows)\n' \
                    '{content}'.format(
                        filename=filename,
                        content=config_file,
                        value=config_value,
                    )

        # ensure this project itself stays up-to-date with the template
        if framework in ['Django', 'Flask']:
            verify_file_matches_repo_root(result, 'tests', 'README.rst')

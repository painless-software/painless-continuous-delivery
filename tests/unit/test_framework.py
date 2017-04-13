"""Tests for generating a Web framework project."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


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
                'requirements.txt',
                'manage.py',
                'application/wsgi.py',
                'config/application/Dockerfile',
                'config/application/uwsgi.ini',
                'config/webserver/Dockerfile',
                'config/webserver/nginx.conf',
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
            'required_files': [
                'requirements.txt',
                'runserver.py',
                'application/wsgi.py',
                'config/application/Dockerfile',
                'config/application/uwsgi.ini',
                'config/webserver/Dockerfile',
                'config/webserver/nginx.conf',
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
            'required_files': [
                'composer.json',
                'composer.lock',
                'config/webserver/Dockerfile',
                'config/webserver/php.ini',
                'src/.htaccess',
                'src/AppBundle/AppBundle.php',
                'web/.htaccess',
                'web/app.php',
            ],
            'install_commands': [
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_framework(self, cookies, project_slug, vcs_account, vcs_platform,
                       ci_service, framework, required_files,
                       install_commands):
        """
        Generate a framework project and verify it is complete and working.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'vcs_platform': vcs_platform,
            'vcs_account': vcs_account,
            'ci_service': ci_service,
            'framework': framework,
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

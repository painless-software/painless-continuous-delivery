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
            ],
        }),
    ]

    # pylint: disable=too-many-arguments,too-many-locals,no-self-use
    def test_framework(self, cookies, project_slug, vcs_account, vcs_platform,
                       ci_service, framework, required_files):
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

        requirements_txt = result.project.join('requirements.txt')
        assert requirements_txt.isfile()
        exit_code = system('pip install -r %s' % requirements_txt)
        assert exit_code == 0, 'Installing requirements fails.'

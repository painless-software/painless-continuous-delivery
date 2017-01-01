"""Tests for correctly generated, working setup."""
from os import system

from . import pytest_generate_tests  # noqa, pylint: disable=unused-import


# pylint: disable=too-few-public-methods
class TestTestSetup(object):
    """
    Tests for verifying generated test setups of this cookiecutter,
    executed several times with different values (test scenarios).
    """
    scenarios = [
        ('django', {
            'project_slug': 'django-project',
            'framework': 'Django',
        }),
        # ('flask', {
        #     'project_slug': 'flask-project',
        #     'framework': 'Flask',
        # }),
    ]

    # pylint: disable=no-self-use
    def test_test_setup(self, cookies, project_slug, framework):
        """
        Generate a project and verify the test setup executes successfully.
        """
        result = cookies.bake(extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'tests': 'flake8,pylint,py35,behave',
        })

        assert result.exit_code == 0
        assert result.exception is None

        tox_ini = result.project.join('tox.ini')
        assert tox_ini.isfile()

        exit_code = system('tox -c %s' % tox_ini)
        assert exit_code == 0, 'Running tests in generated project fails.'

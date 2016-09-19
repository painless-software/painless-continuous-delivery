"""Test generating a project."""
import os


def test_generate_project(cookies):
    """Generate a project with cookiecutter and verify it's complete."""
    os.system('git config --list')
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project.basename == 'name-of-the-project'
    assert result.project.isdir()
    assert result.project.join('README.rst').isfile()

    assert result.project.join('.git').isdir()
    assert result.project.join('.gitignore').isfile()
    # git_config = result.project.join('.git', 'config').readlines(cr=False)
    # repo_remote = 'git@bitbucket.org:company-or-username/name-of-project.git'
    # assert '[remote "origin"]' in git_config
    # assert '\turl = {}'.format(repo_remote) in git_config

    tox_ini = result.project.join('tox.ini').readlines(cr=False)
    assert '[tox]' in tox_ini
    assert 'envlist = flake8,py27,py33,py34,py35,pypy' in tox_ini
    assert '[testenv]' in tox_ini
    assert '[testenv:flake8]' in tox_ini
    assert '[testenv:prospector]' in tox_ini
    assert '[testenv:pylint]' in tox_ini

    ci_service_conf = result.project.join('.travis.yml').readlines(cr=False)
    assert 'script: tox -e $TOX_ENV' in ci_service_conf

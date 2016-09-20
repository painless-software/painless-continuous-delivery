"""Test generating a project."""
from os.path import dirname, join
from filecmp import cmp as compare_files


def test_generate_project(cookies):
    """Generate a project with cookiecutter and verify it's complete."""
    result = cookies.bake(extra_context={
        'tests': 'flake8,prospector,pylint,py27,py33,py34,py35,pypy',
    })

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project.basename == 'name-of-the-project'
    assert result.project.isdir()
    assert result.project.join('README.rst').isfile()

    assert result.project.join('.git').isdir()
    assert result.project.join('.gitignore').isfile()
    git_config = result.project.join('.git', 'config').readlines(cr=False)
    assert '[remote "origin"]' in git_config
    assert '\turl = git@bitbucket.org:' \
           'company-or-username/name-of-the-project.git' in git_config

    tox_ini = result.project.join('tox.ini').readlines(cr=False)
    assert '[tox]' in tox_ini
    assert 'envlist =' \
           ' flake8,prospector,pylint,py27,py33,py34,py35,pypy' in tox_ini
    assert '[testenv]' in tox_ini
    assert '[testenv:flake8]' in tox_ini
    assert '[testenv:prospector]' in tox_ini
    assert '[testenv:pylint]' in tox_ini

    ci_service_conf = result.project.join('.travis.yml').readlines(cr=False)
    assert 'script: tox' in ci_service_conf

    # ensure this project itself stays up-to-date with the template
    for filename in ['tox.ini', '.travis.yml']:
        mother_file = join(dirname(dirname(__file__)), filename)
        generated_file = result.project.join(filename).strpath
        assert compare_files(mother_file, generated_file), \
            "Mother project '{}' not matching template.\n {} != {}".format(
                filename, mother_file, generated_file)

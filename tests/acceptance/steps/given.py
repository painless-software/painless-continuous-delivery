"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""
from cookiecutter.main import cookiecutter
from os.path import join, isfile
from sys import version_info


@given(u'I have just created a {framework} project with this cookiecutter')  # noqa
def step_impl(context, framework):
    major, minor = version_info[:2]
    py_version = 'py%s%s' % (major, minor)
    project_slug = 'painless-%s-%s-project' % (py_version, framework.lower())
    context.logfile = join(context.temp_dir, project_slug + '.log')

    context.generated_dir = cookiecutter(
        template=context.project_dir,
        output_dir=context.temp_dir,
        no_input=True,
        extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'tests': 'flake8,pylint,%s,behave' % py_version,
        })


@given(u'all the configuration files for the test setup are in place')  # noqa
def step_impl(context):
    context.tox_ini = join(context.generated_dir, 'tox.ini')
    assert isfile(context.tox_ini)

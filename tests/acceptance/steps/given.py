"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""
from cookiecutter.main import cookiecutter
from os import chdir, system
from os.path import join, isfile
from sys import version_info


@given('I have just created a {framework} project checking {checks} and testing {tests}')  # noqa
def step_impl(context, framework, checks, tests):
    if 'py_local_' in tests:
        # use active/local Python version to make Vexor CI pass
        major, minor = version_info[:2]
        py_version = 'py%s%s' % (major, minor)
        tests = tests.replace('py_local_', py_version)

    project_slug = 'painless-%s-project' % framework.lower()
    context.logfile = join(context.temp_dir, project_slug + '.log')

    context.generated_dir = cookiecutter(
        template=context.project_dir,
        output_dir=context.temp_dir,
        no_input=True,
        extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'checks': checks,
            'tests': tests,
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
        })


@given('the test environment has been initialized with {setupcommand}')  # noqa
def step_impl(context, setupcommand):
    chdir(context.generated_dir)
    system('{command} > {logfile} 2>&1'.format(
        command=setupcommand,
        logfile=context.logfile,
    ))

    with open(context.logfile) as logfile:
        context.log = logfile.read()


@given('all the configuration files for the test setup are in place')  # noqa
def step_impl(context):
    tox_ini = join(context.generated_dir, 'tox.ini')
    assert isfile(tox_ini)

"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""
from cookiecutter.main import cookiecutter
from os import chdir, system
from os.path import join
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


@given('system libraries have been installed for developing with PHP')  # noqa
def step_impl(context):
    assert system('php --version > /dev/null') == 0, 'PHP not installed.'
    assert system('php --info | grep "Zend Multibyte Support '
                  '=> provided by mbstring" > /dev/null') == 0, \
        'mbstring missing. Try: apt-get install php7.0-mbstring'

    chdir(context.generated_dir)
    system('composer install > {logfile} 2>&1'.format(
        logfile=context.logfile))
    with open(context.logfile) as logfile:
        context.log = logfile.read()

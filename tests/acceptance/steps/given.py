"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""
from os import system
from cookiecutter.main import cookiecutter


@given('I have just created a {framework} {database} project checking {checks} and testing {tests}')  # noqa
def step_impl(context, framework, database, checks, tests):

    project_slug = 'painless-%s-project' % framework.lower()
    context.set_logfilename(project_slug)

    context.generated_dir = cookiecutter(
        template=context.project_dir,
        output_dir=context.temp_dir,
        no_input=True,
        extra_context={
            'project_slug': project_slug,
            'framework': framework,
            'database': database,
            'checks': checks,
            'tests': tests,
            'vcs_platform': 'GitLab.com',
            'ci_service': '.gitlab-ci.yml',
        })


@given('system libraries have been installed for developing with PHP')  # noqa
def step_impl(context):
    php7_installed = (system('php --version | grep "^PHP 7" > /dev/null') == 0)
    if not php7_installed:
        system('sudo apt-get install -y php7.0-cli')

    mbstring_installed = (system('php --info | grep "Zend Multibyte Support '
                                 '=> provided by mbstring" > /dev/null') == 0)
    if not mbstring_installed:
        system('sudo apt-get install -y php7.0-mbstring')

    composer_installed = (system('composer --version > /dev/null') == 0)
    if not composer_installed:
        system('sudo apt-get install -y composer')

    with context.safe_chdir(context.generated_dir):
        exit_code = system('composer install > {logfile} 2>&1'.format(
            logfile=context.logfile))
    if exit_code != 0:
        with open(context.logfile) as logfile:
            context.log = logfile.read()
        print(context.log)


@given('my computer is set up for development with Docker')  # noqa
def step_impl(context):
    assert system('docker --version > /dev/null') == 0, \
        'Docker not found.'
    assert system('docker-compose --version > /dev/null') == 0, \
        'Docker Compose not found.'


@given('I want to work on a {framework} project')  # noqa
def step_impl(context, framework, checks='phpcs', tests='phpunit'):
    context.execute_steps(
        '''
        {given} a {framework} project checking {checks} and testing {tests}
        And system libraries have been installed for developing with PHP
        '''.format(
            given='Given I have just created',
            framework=framework,
            checks=checks,
            tests=tests)
    )


@given('I have just created a Django project')  # noqa
def step_impl(context):
    project_slug = 'painless-deployable-project'
    context.set_logfilename(project_slug)

    context.generated_dir = cookiecutter(
        template=context.project_dir,
        output_dir=context.temp_dir,
        no_input=True,
        extra_context={
            'project_slug': project_slug,
            'framework': 'Django',
            'cronjobs': 'complex',
            'cloud_platform': 'Rancher',
        })

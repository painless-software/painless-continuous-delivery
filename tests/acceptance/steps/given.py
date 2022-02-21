"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""

from cookiecutter.main import cookiecutter


@given('I have just created a {framework} {database} project checking {checks} and testing {tests}')  # noqa
def step_impl(context, framework, database, checks, tests):

    project_slug = f'painless-{framework.lower()}-project'
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

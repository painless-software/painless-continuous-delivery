"""
'When' step implementations for acceptance tests.  Powered by behave.
"""


@when('I run the test suite with {commands}')  # noqa
def step_impl(context, commands):
    testsuite = [cmd.strip() for cmd in commands.split('&&')]

    with context.safe_chdir(context.generated_dir):
        for command in testsuite:
            context.log_run(command)


@when('I run {command}')  # noqa
def step_impl(context, command):
    with context.safe_chdir(context.generated_dir):
        context.log_run(command)


@when('I generate the deployment configuration')  # noqa
def step_impl(context):
    with context.safe_chdir(context.generated_dir):
        context.log_run('kustomize build')

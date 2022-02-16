"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from pathlib import Path


@when('I run the test suite with {commands}')  # noqa
def step_impl(context, commands):
    testsuite = [cmd.strip() for cmd in commands.split('&&')]

    with context.safe_chdir(context.generated_dir):
        for command in testsuite:
            context.log_run(command)

            assert context.exit_code == 0, \
                f"Command failed with error:\n{context.log}"


@when('I run {command}')  # noqa
def step_impl(context, command):
    with context.safe_chdir(context.generated_dir):
        context.log_run(command)

    assert context.exit_code == 0, \
        f"Command failed with error:\n{context.log}"


@when('I generate the deployment manifests')  # noqa
def step_impl(context):
    with context.safe_chdir(context.generated_dir):
        deploy_dir = Path('.') / 'manifests' / 'application' / 'overlays' / 'production'  # noqa
        context.log_run(f'kustomize build {deploy_dir}')

    assert context.exit_code == 0, \
        f"Command failed with error:\n{context.log}"

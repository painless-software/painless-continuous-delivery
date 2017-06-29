"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from os import chdir, system


@when('I run the test suite with {commands}')  # noqa
def step_impl(context, commands):
    chdir(context.generated_dir)
    testsuite = [cmd.strip() for cmd in commands.split('&&')]

    for command in testsuite:
        context.exit_code = system('{command} > {logfile} 2>&1'.format(
            command=command,
            logfile=context.logfile,
        ))
        with open(context.logfile) as logfile:
            context.log = logfile.read()

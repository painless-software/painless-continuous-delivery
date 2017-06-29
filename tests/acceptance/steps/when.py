"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from os import chdir, system


@when('I run the test suite with {testsuite}')  # noqa
def step_impl(context, testsuite):
    chdir(context.generated_dir)
    context.exit_code = system('{command} > {logfile} 2>&1'.format(
        command=testsuite,
        logfile=context.logfile,
    ))

    with open(context.logfile) as logfile:
        context.log = logfile.read()

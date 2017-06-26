"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from behave import when
from os import system


@when(u'I run the test suite')
def step_impl(context):
    context.exit_code = system('tox -c {config} > {logfile}'.format(
        config=context.tox_ini,
        logfile=context.logfile,
    ))

    with open(context.logfile) as logfile:
        context.log = logfile.read()

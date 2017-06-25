"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from behave import when
from os import system


@when(u'I run the test suite')
def step_impl(context):
    context.exit_code = system('tox -c %s' % context.tox_ini)

"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from behave import when


@when(u'I run the test suite')
def step_impl(context):
    assert True, "Implementation of a test action expected."

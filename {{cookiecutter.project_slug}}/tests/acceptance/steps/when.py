"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from behave import when


@when(u'I log in with username and password')
def step_impl(context):
    assert True, "Implementation of a test action expected."

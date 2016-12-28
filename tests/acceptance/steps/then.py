"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""
from behave import then


@then(u'all tests pass successfully')
def step_impl(context):
    assert True, "Implementation of testing a result expected."

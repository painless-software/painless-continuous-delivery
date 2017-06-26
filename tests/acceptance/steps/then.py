"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""
from behave import then


@then(u'all tests pass successfully')
def step_impl(context):
    assert context.exit_code == 0, \
        'Running tests in generated project fails.\n' \
        '----------------- (log follows)\n' \
        '%s' % context.log

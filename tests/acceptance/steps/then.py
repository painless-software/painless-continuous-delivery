"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""


@then(u'all tests pass successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        'Running tests in generated project fails.\n' \
        '----------------- (log follows)\n' \
        '%s' % context.log

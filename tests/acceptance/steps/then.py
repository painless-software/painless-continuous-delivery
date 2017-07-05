"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""
import requests


@then('all tests pass successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        context.explain_log('Running tests in generated project fails.')


@then('all images are built successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        context.explain_log('Docker build fails.')

    assert 'Successfully built' in context.log
    assert 'Successfully built' in context.log


@then('the project starts up successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        context.explain_log('Docker Compose up fails with exit code %s.' %
                            context.exit_code)

    with context.safe_chdir(context.generated_dir):
        context.log_run('docker-compose ps')

    started_services = len(context.log.split(' Up   ')) - 1
    assert context.exit_code == 0 and started_services == 2, \
        context.explain_log('Not all services are starting up successfully.')


@then('the application is available at {applicationurl}')  # noqa
def step_impl(context, applicationurl):
    r = requests.get(applicationurl)
    assert r.status_code == 200, \
        'Application returns status code %s' % r.status_code

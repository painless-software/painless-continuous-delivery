"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""

import requests


@then('all tests pass successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        context.explain_log('Running tests in generated project fails.')


@then(u'a {dotenv} file is created with UID/GID values')  # noqa
def step_impl(context, dotenv):
    assert context.exit_code == 0, \
        context.explain_log('Command fails with exit code %s.' %
                            context.exit_code)

    with context.safe_chdir(context.generated_dir):
        with open(dotenv) as dotenvfile:
            content = dotenvfile.read()
            assert 'LOCAL_UID=' in content
            assert 'LOCAL_GID=' in content


@then('all images are built successfully')  # noqa
def step_impl(context):
    assert context.exit_code == 0, \
        context.explain_log('Docker build fails.')

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


@then('the application is available at {appurl} showing {appcontent}')  # noqa
def step_impl(context, appurl, appcontent):
    resp = requests.get(appurl, appcontent, timeout=60)
    assert resp.status_code == 200, \
        'Application returns status code %s' % resp.status_code

    response_body = resp.content.decode('utf-8')
    assert appcontent in response_body, \
        "Application doesn't show expected content: {expected}\n" \
        "----------------- (response body follows)\n" \
        "{body}".format(expected=appcontent, body=response_body)


@then('it contains the expected Kubernetes objects')  # noqa
def step_impl(context):
    expected_kinds = [
        'ConfigMap',
        'CronJob',
        'Deployment',
        'Ingress',
        'RoleBinding',
        'Secret',
        'Service',
    ]
    for kind in expected_kinds:
        needle = 'kind: %s\n' % kind
        assert needle in context.log, \
            "Kind '%s' missing in configuration\n\n%s" % (kind, context.log)

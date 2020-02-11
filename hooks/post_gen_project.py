"""Post-generate hook for cookiecutter."""
from os import listdir, remove
from os.path import join
from pathlib import Path
from subprocess import CalledProcessError, check_call, check_output, STDOUT

import contextlib
import logging
import shutil
import sys


def shell(command, capture=False):
    """Portable system call that aborts generation in case of failure."""
    try:
        if capture:
            stdout = check_output(command, shell=True, stderr=STDOUT,
                                  universal_newlines=True)
            return str(stdout)

        return check_call(command, shell=True)
    except CalledProcessError as err:
        LOG.error('Project generation failed.')
        sys.exit(err.returncode)


def get_framework_and_technology():
    """
    Returns the framework and its related technology (e.g. Django, python)
    as a tuple. Fails with a ``KeyError`` if no framework is specified.
    """
    framework_technology = {
        'Django': 'python',
        'Flask': 'python',
        'Symfony': 'php',
        'TYPO3': 'php',
    }
    framework = '{{ cookiecutter.framework }}'

    return framework, framework_technology[framework]


def set_up_ci_service():
    """If a framework project was created move it to project root."""
    ci_service = '{{ cookiecutter.ci_service }}'

    if ci_service == 'codeship-steps.yml':
        LOG.info('Adding additional files for this CI setup ...')
        ci_services_folder = join('_', 'ci-services')
        shutil.move(join(ci_services_folder, 'codeship-services.yml'), '.')


def set_up_framework_and_tests():
    """If a framework project was created move it to project root."""
    try:
        framework, technology = get_framework_and_technology()
    except KeyError:
        LOG.warning('Skipping framework and test setup: '
                    'No framework specified.')
        return

    LOG.info('Moving files for %s project ...', framework)
    framework_folder = join('_', 'frameworks', framework)
    for file_or_folder in listdir(framework_folder):
        shutil.move(join(framework_folder, file_or_folder), '.')

    LOG.info('Moving test setup for %s project ...', framework)
    with contextlib.suppress(FileNotFoundError):
        testing_folder = join('_', 'testing', technology)
        for file_or_folder in listdir(testing_folder):
            shutil.move(join(testing_folder, file_or_folder), '.')


def prune_cronjob_style():
    """
    Based on selected cronjob setup style, remove the other unneeded files.
    """
    cron_type = '{{ cookiecutter.cronjobs }}'
    base_path = join('deployment', 'application', 'base')

    with contextlib.suppress(FileNotFoundError):
        if cron_type != 'simple':
            remove(join(base_path, 'cronjob.yaml'))
        if cron_type != 'complex':
            shutil.rmtree(join(base_path, 'cronjob'))


def set_up_deployment():
    """
    If a framework project was created also move deployment configuration
    to project root.
    """
    try:
        framework, technology = get_framework_and_technology()
    except KeyError:
        LOG.warning('Skipping deployment configuration: '
                    'No framework specified.')
        return

    LOG.info('Moving deployment configuration for %s project ...', framework)
    deployment = 'deployment'
    shutil.move(join('_', 'deployment'), deployment)
    prune_cronjob_style()

    for elem in listdir(deployment):
        destination = Path(deployment) / elem
        technology_folder = destination / '_' / technology

        with contextlib.suppress(FileNotFoundError, NotADirectoryError):
            for file_or_folder in listdir(str(technology_folder)):
                src = technology_folder / file_or_folder
                shutil.move(str(src), str(destination))

            shutil.rmtree(str(technology_folder.parent))


def set_up_dev_tooling():
    """
    Move tooling from the development folder to the project root.
    """
    try:
        framework, technology = get_framework_and_technology()
    except KeyError:
        LOG.warning('Skipping development toolimg setup: '
                    'No framework specified.')
        return

    LOG.info('Moving development tooling for %s project ...', framework)
    development_folder = join('_', 'development', technology)
    for file_or_folder in listdir(development_folder):
        shutil.move(join(development_folder, file_or_folder), '.')


def remove_temporary_files():
    """Remove files and folders only needed as input for generation."""
    LOG.info('Removing input data folder ...')
    shutil.rmtree('_')


def init_version_control():
    """Initialize a repository, commit the code, and prepare for pushing."""
    vcs_info = {
        'platform_name': '{{ cookiecutter.vcs_platform }}',
        'platform': '{{ cookiecutter.vcs_platform.lower() }}',
        'account': '{{ cookiecutter.vcs_account }}',
        'project': '{{ cookiecutter.project_slug }}',
    }
    vcs_info['remote_uri'] = \
        'git@{platform}:{account}/{project}.git'.format(**vcs_info)
    vcs_info['web_url'] = \
        'https://{platform}/{account}/{project}'.format(**vcs_info)

    LOG.info('Initializing version control ...')
    shell('git init --quiet')
    shell('git add .')

    output = shell('git config --list', capture=True)
    if 'user.email=' not in output:
        LOG.warning('I need to add user.email. BEWARE! Check with:'
                    ' git config --list')
        shell('git config user.email "{{ cookiecutter.email }}"')
    if 'user.name=' not in output:
        LOG.warning('I need to add user.name. BEWARE! Check with:'
                    ' git config --list')
        shell('git config user.name "{{ cookiecutter.full_name }}"')

    shell('git commit --quiet'
          ' -m "Initial commit by Painless Continuous Delivery"')
    shell('git remote add origin {remote_uri}'.format(**vcs_info))
    LOG.info("You can now create a project '%(project)s' on %(platform_name)s."
             " %(web_url)s", vcs_info)
    LOG.info('Then push the code to it: git push -u origin --all')


def deploy_field_test():
    """
    Push the generated project to the target repo. Trigger this action
    using the ``push`` parameter, e.g. ``cookiecutter ... push=force``.
    """
    if '{{ cookiecutter.push }}' == 'automatic':
        shell('git push origin master')
    elif '{{ cookiecutter.push }}' == 'force':
        shell('git push origin master --force')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    LOG = logging.getLogger('post_gen_project')

    set_up_ci_service()
    set_up_framework_and_tests()
    set_up_deployment()
    set_up_dev_tooling()
    remove_temporary_files()
    init_version_control()
    deploy_field_test()

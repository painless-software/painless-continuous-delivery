# pylint: disable=comparison-of-constants
"""Post-generate hook for cookiecutter."""

import logging
import shutil
import sys
from pathlib import Path
from subprocess import CalledProcessError, run


class Shell:  # pylint: disable=too-few-public-methods
    """
    Command execution shell as a class to allow preserving behavior across
    execution calls.
    """

    def __init__(self, cwd=None, capture=False):
        """A shell executed from a specific directory (default: current)."""
        self.cwd = cwd
        self.capture = capture

    def run(self, command):
        """Portable system call that aborts generation in case of failure."""
        try:
            return run(
                command,
                capture_output=self.capture,
                check=True,
                cwd=self.cwd,
                shell=True,
                text=True,
            )
        except CalledProcessError as err:
            LOG.error('Project generation failed.')
            sys.exit(err.returncode)


def get_framework_and_technology():
    """
    Return the framework and its related technology (e.g. Django, python) as
    a tuple.  Fails with a ``KeyError`` if user didn't choose a framework.
    """
    framework_technology = {
        'Django': 'python',
        'Flask': 'python',
        'SpringBoot': 'java',
    }
    framework = '{{ cookiecutter.framework }}'

    return framework, framework_technology[framework]


def set_up_framework_and_tests():
    """
    If a framework project was created move it to project root.
    """
    try:
        framework, technology = get_framework_and_technology()
    except KeyError:
        LOG.warning('Skipping framework and test setup: '
                    'No framework specified.')
        return

    LOG.info('Moving files for %s project ...', framework)
    framework_folder = Path('_') / 'frameworks' / framework
    if framework_folder.exists():
        for file_or_folder in framework_folder.iterdir():
            shutil.move(str(file_or_folder), '.')

    LOG.info('Moving test setup for %s project ...', framework)
    testing_folder = Path('_') / 'testing' / technology
    if testing_folder.exists():
        for file_or_folder in testing_folder.iterdir():
            shutil.move(str(file_or_folder), '.')


def prune_cronjob_style():
    """
    Based on selected cronjob setup style, remove the other unneeded files.
    """
    cron_type = '{{ cookiecutter.cronjobs }}'
    base_path = Path('manifests') / 'application' / 'base'

    if cron_type != 'simple':
        (base_path / 'cronjob.yaml').unlink()
    if cron_type != 'complex':
        shutil.rmtree(base_path / 'cronjob')


def prune_route_or_ingress():
    """
    Based on selected target cloud platform, remove the other unneeded files.
    """
    app_manifests = Path('manifests') / 'application'
    base_path = app_manifests / 'base'
    development_path = app_manifests / 'overlays' / 'development'
    integration_path = app_manifests / 'overlays' / 'integration'
    production_path = app_manifests / 'overlays' / 'production'

    if '{{ cookiecutter.cloud_platform }}' not in ['Rancher']:
        (base_path / 'ingress.yaml').unlink()
        (development_path / 'ingress-patch.yaml').unlink()
        (integration_path / 'ingress-patch.yaml').unlink()

    if '{{ cookiecutter.cloud_platform }}' not in ['APPUiO']:
        (base_path / 'route.yaml').unlink()
        (base_path / 'route-crd.yaml').unlink()
        (production_path / 'route.yaml').unlink()


def flatten_folder_structure(folder, technology):
    """
    Integrate content from subfolders with special meaning (underscore
    folders) into the parent folder.
    """
    subfolders = [_ for _ in folder.iterdir() if _.is_dir()]

    for config in [folder] + subfolders:
        technology_folder = config / '_' / technology
        if technology_folder.parent.exists():
            if technology_folder.exists():
                for file_or_folder in technology_folder.iterdir():
                    shutil.move(str(file_or_folder), config)
            shutil.rmtree(technology_folder.parent)


def set_up_manifests():
    """
    If a framework project was created also move deployment manifests
    to project root.
    """
    manifests = Path('manifests')
    try:
        framework, technology = get_framework_and_technology()
    except KeyError:
        LOG.warning('Removing deployment manifests: '
                    'No framework specified.')
        shutil.rmtree(manifests)
        return

    LOG.info('Set up deployment manifests for %s project ...', framework)
    prune_cronjob_style()
    prune_route_or_ingress()
    flatten_folder_structure(manifests, technology)


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
    development_folder = Path('_') / 'development' / technology
    for file_or_folder in development_folder.iterdir():
        shutil.move(str(file_or_folder), '.')


def remove_temporary_files():
    """
    Remove files and folders only needed as input for generation.
    """
    LOG.info('Removing input data folder ...')
    shutil.rmtree('_')
    shutil.rmtree(Path('gitops') / '_')

    if '{{ cookiecutter.database }}' == '(none)':
        shutil.rmtree(Path('manifests') / 'database', ignore_errors=True)
        shutil.rmtree(Path('gitops') / 'database')


def merge_folder_into(src_dir, dest_dir):
    """
    Move all files of a directory into a target directory.
    """
    source, destination = Path(src_dir), Path(dest_dir)

    for file_or_folder in source.iterdir():
        target = destination / file_or_folder.name

        if file_or_folder.is_dir() and target.exists():
            merge_folder_into(file_or_folder, target)
        elif not target.exists():
            file_or_folder.rename(target)
        else:
            raise FileExistsError(target)

    source.rmdir()


def move_appconfigs_to_gitops():
    """
    Add manifests for all deployed components to the GitOps setup.
    """
    directories = [_ for _ in Path('manifests').iterdir() if _.is_dir()]

    for app_config in directories:
        target = Path('gitops') / app_config.name
        merge_folder_into(app_config, target)
    shutil.rmtree(Path('manifests'))


def move_gitops_repo():
    """
    Delete gitops folder in case a monorepo is used, or move gitops folder
    outside the application repository in case gitops strategy is used.
    """
    if '{{ cookiecutter.deployment_strategy }}' == "gitops":
        gitops_folder = Path.cwd().parent / '{{ cookiecutter.gitops_project }}'

        LOG.info('Setting up GitOps repository ...')
        move_appconfigs_to_gitops()
        shutil.move('gitops', gitops_folder)
    else:
        shutil.rmtree('gitops')


def init_version_control():
    """
    Put all code we generate conveniently under version control.
    """
    init_version_control_for('{{ cookiecutter.project_slug }}',
                             '{{ cookiecutter.vcs_project }}')
    if '{{ cookiecutter.deployment_strategy }}' == "gitops":
        init_version_control_for('{{ cookiecutter.gitops_project }}',
                                 '{{ cookiecutter.gitops_project }}')


def init_version_control_for(local_project, remote_project):
    """
    Initialize a repository, commit the code, and prepare for pushing.
    """
    vcs_info = {
        'platform_name': '{{ cookiecutter.vcs_platform }}',
        'platform': '{{ cookiecutter.vcs_platform.lower() }}',
        'account': '{{ cookiecutter.vcs_account }}',
        'project': remote_project,
    }
    vcs_info['remote_uri'] = \
        'git@{platform}:{account}/{project}.git'.format(**vcs_info)
    vcs_info['web_url'] = \
        'https://{platform}/{account}/{project}'.format(**vcs_info)

    repo_path = Path.cwd().parent / local_project
    silent_shell = Shell(repo_path, capture=True)
    shell = Shell(repo_path)

    LOG.info('Initializing version control ...')
    shell.run('git init --quiet')
    shell.run('git add .')

    output = silent_shell.run('git config --list').stdout
    if 'user.email=' not in output:
        LOG.warning('I need to add user.email. BEWARE! Check with:'
                    ' git config --list')
        shell.run('git config user.email "{{ cookiecutter.email }}"')
    if 'user.name=' not in output:
        LOG.warning('I need to add user.name. BEWARE! Check with:'
                    ' git config --list')
        shell.run('git config user.name "{{ cookiecutter.full_name }}"')

    shell.run('git commit --quiet'
              ' -m "Initial commit by Painless Continuous Delivery"')
    shell.run('git remote add origin %(remote_uri)s' % vcs_info)
    LOG.info("You can now create a project '%(project)s' on %(platform_name)s."
             " %(web_url)s", vcs_info)
    LOG.info('Then push the code to it: git push -u origin --all')


def deploy_field_test():
    """
    Push all generated code to the target repositories.
    """
    deploy_field_test_for("{{ cookiecutter.project_slug }}")
    if '{{ cookiecutter.deployment_strategy }}' == "gitops":
        deploy_field_test_for("{{ cookiecutter.gitops_project }}")


def deploy_field_test_for(local_project):
    """
    Push the generated project to the target repo. Trigger this action
    using the ``push`` parameter, e.g. ``cookiecutter ... push=force``.
    """
    repo_path = Path.cwd().parent / local_project
    shell = Shell(repo_path)

    if '{{ cookiecutter.push }}' == 'automatic':
        shell.run('git push origin main')
    elif '{{ cookiecutter.push }}' == 'force':
        shell.run('git push origin main --force')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    LOG = logging.getLogger('post_gen_project')

    if sys.version_info < (3, 7):
        msg = "Python 3.7+ required. ABORTING."
        raise SystemExit(msg)

    set_up_framework_and_tests()
    set_up_manifests()
    set_up_dev_tooling()
    remove_temporary_files()
    move_gitops_repo()
    init_version_control()
    deploy_field_test()

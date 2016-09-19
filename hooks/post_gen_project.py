"""Post-generate hook for cookiecutter."""
from subprocess import CalledProcessError, check_call, check_output, STDOUT

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
        else:
            check_call(command, shell=True)
    except CalledProcessError as err:
        LOG.error('Project generation failed.')
        sys.exit(err.returncode)


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
    LOG.info('Then push the code to it: $ git push -u origin --all')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    LOG = logging.getLogger('post_gen_project')

    remove_temporary_files()
    init_version_control()

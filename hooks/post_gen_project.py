"""
Post-generate hook for cookiecutter
"""
import logging
import os
import shutil

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('post_gen_project')

logger.info('Removing input data folder ...')
shutil.rmtree('_')

logger.info('Initializing version control ...')
vcs_info = {
    'platform_name': '{{ cookiecutter.vcs_platform }}',
    'platform': '{{ cookiecutter.vcs_platform.lower() }}',
    'account': '{{ cookiecutter.vcs_account }}',
    'project': '{{ cookiecutter.project_slug }}',
}
vcs_info['remote_uri'] = 'git@{platform}:{account}/{project}.git'.format(**vcs_info)
vcs_info['web_url'] = 'https://{platform}/{account}/{project}'.format(**vcs_info)

success = os.system(
    "git init --quiet && "
    "git add . && "
    "git commit --quiet -m 'Initial commit by Painless Continuous Delivery' && "
    "git remote add origin {remote_uri}".format(**vcs_info)
)
logger.info("You can now create a project '{project}' on {platform_name}."
            " {web_url}".format(**vcs_info))
logger.info('Then push the code to it: $ git push -u origin --all')

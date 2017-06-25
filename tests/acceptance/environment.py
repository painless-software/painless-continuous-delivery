"""
Painless environment setup for acceptance tests.  Powered by behave.
Visit the docs at
https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
"""
from os.path import dirname
from tempfile import mkdtemp
from shutil import rmtree


def before_all(context):
    """
    Before the first test starts, find out and create directory paths we want
    to use.
    """
    context.project_dir = dirname(dirname(dirname(__file__)))
    context.temp_dir = mkdtemp(prefix='painless-acceptance-tests-')


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    pass


def after_all(context):
    """
    After all tests, do cleanup work.
    """
    rmtree(context.temp_dir)

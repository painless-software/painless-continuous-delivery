"""
Painless environment setup for acceptance tests.  Powered by behave.
Visit the docs at
https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
"""
from contextlib import contextmanager
from os import chdir, getcwd, system
from os.path import dirname, join
from shutil import rmtree
from tempfile import mkdtemp


def before_all(context):
    """
    Before the first test starts, find out and create directory paths we want
    to use.
    """
    @contextmanager
    def safe_chdir(path):
        """Restore the original directory when leaving the with-clause"""
        old_path = getcwd()
        chdir(path)
        try:
            yield
        finally:
            chdir(old_path)

    def set_logfilename(name):
        """Set the logfile context value using for logging system calls"""
        context.logfile = join(context.temp_dir, name + '.log')

    def log_run(command):
        """Run system commands, log their output, return the exit status"""
        context.exit_code = system('{command} > {logfile} 2>&1'.format(
            command=command,
            logfile=context.logfile,
        ))
        with open(context.logfile) as logfile:
            context.log = logfile.read()
        return context.exit_code

    def explain_log(message):
        """Helper function for assertions"""
        return '{message}\n' \
               '----------------- (log follows)\n' \
               '{log}'.format(message=message, log=context.log)

    context.safe_chdir = safe_chdir
    context.set_logfilename = set_logfilename
    context.log_run = log_run
    context.explain_log = explain_log

    context.project_dir = dirname(dirname(dirname(__file__)))
    context.temp_dir = mkdtemp(prefix='painless-acceptance-tests-')


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    """
    Clean up cookiecutter data after each scenario.
    """
    if context.generated_dir:
        rmtree(context.generated_dir)


def after_all(context):
    """
    After all tests, do cleanup work.
    """
    rmtree(context.temp_dir)

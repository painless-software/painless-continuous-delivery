Tests
=====

    Software without tests is broken by design.

    -- https://painless.software/writing-tests

Philosophy
----------

No need to install additional packages for running tests
    All dependencies for running your tests are specified in ``tox.ini``

    `Tox`_ will create virtual environments and install those packages
    automagically when running your tests.

Working with Tox
----------------

Install Tox on your local machine:

.. code-block:: console

    pip install tox

Use the ``tox`` command in the terminal to run your tests locally:

.. code-block:: console

    # list all available test environments (= Tox targets)
    tox -lv

.. code-block:: console

    # run all tests against all environments
    tox

.. code-block:: console

    # run a specific set of tests (one or several)
    tox -e py37
    tox -e flake8,py37

.. code-block:: console

    # remove all environments, build files and folders
    tox -e clean

If you need to use command line options for a command separate them with a
double-dash, like so:

.. code-block:: console

     tox <tox args> -- <command args>

Examples:

.. code-block:: console

    tox -e py36 -- -vv --exitfirst
    tox -e behave -- --format=pretty
    tox -e behave -- --tags=-docker
    tox -e flake8 -- --help

Linting and Unit Tests
----------------------

We use `Tox`_ to run our entire tests suite, including all supported Python
versions.  You may want to use `pyenv`_ to install all Python versions locally.
Alternatively, you can test only against the versions you already have
installed on your machine as follows, wait for the build servers to cover the
missing ones, and fix identified issues (if any) with additional commits:

.. code-block:: console

    tox -e flake8,pylint,py36,py37

Field Tests
-----------

We have field tests to generate and deploy an example project from your
local working version.  In order to run the deployment, you need to have
access to the GitLab repository of your target generated project (such as
`example django`_), and you need to generate a Personal Access Token on
GitLab. (Top-right user menu > Settings > Access Tokens)

.. code-block:: console

    export GITLAB_API_TOKEN=<your personal access token>
    tox -e clean,fieldtest django

Generated files are found in ``/tmp/painless-generated-projects``

Running Docker in Tests
------------------------

Tests that require Docker must be run locally on your developer machine,
because not all CI servers allow running Docker (inside Docker) on their
infrastructure.  In `behave`_ tests the related scenarios are tagged with
``@docker``.  Run them with:

.. code-block:: console

    tox -e behave -- --tags=docker


.. _Tox: https://tox.readthedocs.io/en/latest/
.. _pull request: https://github.com/painless-software/painless-continuous-delivery/pulls
.. _bug tracker: https://github.com/painless-software/painless-continuous-delivery/issues
.. _flake8: http://flake8.readthedocs.io/en/latest/
.. _Pylint: https://pylint.org/
.. _pyenv: https://github.com/yyuu/pyenv#basic-github-checkout
.. _behave: https://behave.readthedocs.io/en/latest/
.. _example django: https://gitlab.com/appuio/example-django

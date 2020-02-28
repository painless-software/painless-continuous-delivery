How To Contribute
=================

If you want to make this piece of software more useful, better fit your needs,
fix bugs or typos your help is greatly appreciated!

- If you have specific changes that should go into the code base please
  prepare a `pull request`_.
- If you're unsure or need to discuss your ideas please open an issue in our
  `bug tracker`_.
- As a general rule, all code changes need to satisfy the default rules
  enforced by `flake8`_ and `Pylint`_ (PEP8 et al.).
- Please add tests and make sure the builds all pass (run ``tox`` locally).

Testing
-------

We use `tox`_ to run tests against all target environments.  You may want to
use `pyenv`_ to test against all Python version locally.  Alternatively, you
can test only against the versions you already have installed on your machine
as follows, wait for the build servers to cover the missing pieces and fix
identified issues with additional commits:

.. code-block:: console

    tox -e flake8,pylint,py36,py37

We have field tests to generate and deploy an example project from your
local working version.  In order to run the deployment, you need to have
access to the GitLab repository of your target generated project (such as
`example django`_), and you need to generate a Personal Access Token on 
GitLab. (Top-right user menu > Settings > Access Tokens)

.. code-block:: console

    export GITLAB_API_TOKEN=<your personal access token>
    tox -e clean,fieldtest -- django

Generated files are found in `/tmp/painless-generated-projects`

Tests that require Docker must be run locally on your developer machine,
because not all CI servers allow running Docker (inside Docker) on their
infrastructure.  In `behave`_ tests the related scenarios are tagged with
``@docker``.  Run them with:

.. code-block:: console

    tox -e behave -- --tags=docker


.. _pull request: https://github.com/painless-software/painless-continuous-delivery/pulls
.. _bug tracker: https://github.com/painless-software/painless-continuous-delivery/issues
.. _flake8: http://flake8.readthedocs.io/en/latest/
.. _Pylint: https://pylint.org/
.. _tox: http://tox.readthedocs.io/en/latest/
.. _pyenv: https://github.com/yyuu/pyenv#basic-github-checkout
.. _behave: https://behave.readthedocs.io/en/latest/
.. _example django: https://gitlab.com/appuio/example-django

Tests
=====

    Software without tests is broken by design.

    -- https://painless.software/writing-tests

Philosophy
----------

No need to install additional packages for running tests
    Add all dependencies for running your tests to ``tests/requirements.txt``.
    (Tox_ will create virtual environments and install those packages
    automagically when running your tests.)

.. _Tox: https://tox.readthedocs.io/en/latest/

Running Your Tests Locally
--------------------------

Install Tox on your local machine:

.. code-block:: bash

    pip install tox

Use the ``tox`` command in the terminal to run your tests locally:

.. code-block:: bash

    # list all available test environments (= Tox targets)
    $ tox -l

.. code-block:: bash

    # run all tests against all environments
    $ tox

.. code-block:: bash

    # run a specific set of tests (one or several)
    $ tox -e py35
    $ tox -e flake8,py35

.. code-block:: bash

    # remove all environments, build files and folders
    $ tox -e clean

If you need to use command line arguments for a command separate them with a
double-dash, like so::

     $ tox <tox args> -- <command args>

Examples:

.. code-block:: bash

    $ tox -e behave -- --format=pretty
    $ tox -e flake8 -- --help

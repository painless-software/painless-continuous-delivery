Skeleton Generator Scripts
==========================

This folder contains scrips or configurations for generating skeletons used in
the cookiecutter project. This functionality is used for development of the
cookiecutter only.

We use Tox, which will install all necessary dependencies for generating the
skeletons in isolated virtual environments. The only thing you need to install
on your cookiecutter development machine is Tox itself:

.. code-block:: bash

    $ pip install tox

General Usage
-------------

.. code-block:: bash

    # list all available skeleton targets (= Tox targets)
    $ tox -l

.. code-block:: bash

    # generate all skeletons in the ./.tox/<target>/_/ folder
    $ tox

.. code-block:: bash

    # list all generated, sanitized skeletons
    $ ls -l .tox/*/_/

.. code-block:: bash

    # remove skeletons, build files and folders
    $ tox -e clean

Django Project Skeletons
------------------------

.. code-block:: bash

    # generate skeleton for a specific Django version
    $ tox -e django18

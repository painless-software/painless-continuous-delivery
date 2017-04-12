Skeleton Generator Scripts
==========================

This folder contains scrips or configurations for generating skeletons used in
the cookiecutter project. This functionality is used for development of the
cookiecutter only.

Philosophy
----------

:LTS versions:

    We focus on LTS versions and try to cover stable versions for any framework
    if this is feasible to do.  *Read:* The skeleton we generate should work
    with all versions from the last LTS up to the current stable version.

:Tox:

    We use Tox, which will install all necessary dependencies for generating the
    skeletons in isolated virtual environments. The only thing you need to
    install on your cookiecutter development machine should be Tox itself:

    .. code-block:: bash

        $ pip install tox

    Technologies other than Python need software installed systemwide, outside
    of virtual environments created by Tox.

General Usage
-------------

.. code-block:: bash

    # list all available skeleton targets (= Tox targets)
    $ tox -l
    # list all skeleton targets for Django
    $ tox -l -c tox-django.ini

.. code-block:: bash

    # generate all skeletons in the ./.tox/<target>/_/ folder
    $ tox
    # generate only skeletons for Django
    $ tox -e django
    # generate only the skeleton for Django 1.11
    $ tox -e django111 -c tox-django.ini

.. code-block:: bash

    # list all generated, sanitized skeletons
    $ ls -l .tox/*/_/

.. code-block:: bash

    # remove skeletons, build files and folders
    $ tox -e clean

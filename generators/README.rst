Skeleton Generator Scripts
==========================

This folder contains scrips or configurations for generating skeletons used
in the cookiecutter project. This functionality is used for the cookiecutter
development only.

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

    # generate project skeleton for a specific Django version
    $ tox -e django18

.. code-block:: bash

    # remove build files and folders
    $ tox -e clean

Django Project Skeletons
------------------------

.. code-block:: bash

    # generate default Django project skeletons
    $ tox

will generate the default Django project skeleton for all supported Django
versions. They will be created in the ``.tox/<django-version>/_`` folder.

.. code-block:: bash

    # list all generated, sanitized Django project skeletons
    $ ls -l .tox/*/_/

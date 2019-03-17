{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Getting Started
---------------

To start developing on this project simply bring up the Docker setup:

.. code-block:: console
{% if cookiecutter.framework == 'Django' %}
    docker-compose up --build -d
    docker-compose exec application python manage.py migrate
    docker-compose logs -f
{% elif cookiecutter.framework in ['Symfony', 'TYPO3'] %}
    composer install
    docker-compose up --build
{% else %}
    docker-compose up --build
{% endif %}
Open your web browser at http://localhost:8000 to see the application
you're developing.  Log output will be displayed in the terminal, as usual.

{% if cookiecutter.container_platform == 'APPUiO' -%}
Initial Setup on APPUiO (OpenShift)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a ``prod`` and ``staging`` project at the `VSHN Control Panel
   <https://control.vshn.net/openshift/projects/appuio%20public>`_.
   For sizing consider roughly the sum of ``limits`` of all resources
   (it must be strictly greater than the sum of ``requests``).
1. Create a service account as described in the `APPUiO docs
   <https://appuio-community-documentation.readthedocs.io/en/latest/services/webserver/50_pushing_to_appuio.html>`_
   (see below)
1. Add the ``token`` value from the ``gitlab-ci-token`` secret to the GitLab
   project Settings > CI/CD > Variables as "OPENSHIFT_TOKEN".

.. code-block:: console

    # Calculate min/max sizing requirements for quotas
    $ grep -A2 limits deployment/*yaml
    $ grep -A2 requests deployment/*yaml

.. code-block:: console

    # Create a service account to allow GitLab CI to push images to the APPUiO registry
    $ oc -n {{ cookiecutter.project_slug }}-prod create sa gitlab-ci

.. code-block:: console

    # Grant permission for pushing Docker images to APPUiO and applying configurations
    $ oc -n {{ cookiecutter.project_slug }}-prod policy add-role-to-user edit -z gitlab-ci
    $ oc -n {{ cookiecutter.project_slug }}-staging policy add-role-to-user edit system:serviceaccount:{{ cookiecutter.project_slug }}-prod:gitlab-ci

.. code-block:: console

    # Get the token value from APPUiO
    $ oc -n {{ cookiecutter.project_slug }}-prod sa get-token gitlab-ci

{% endif -%}
Working with Docker
^^^^^^^^^^^^^^^^^^^

Create/destroy development environment:

.. code-block:: console

    docker-compose up -d    # create and start; omit -d to see log output
    docker-compose down     # docker-compose kill && docker-compose rm -af

Start/stop development environment:

.. code-block:: console

    docker-compose start    # resume after 'stop'
    docker-compose stop     # stop containers, but keep them intact

Other useful commands:

.. code-block:: console

    docker-compose ps       # list running containers
    docker-compose logs -f  # view (and follow) container logs

See the `docker-compose CLI reference`_ for other commands.

.. _docker-compose CLI reference: https://docs.docker.com/compose/reference/overview/

Docker Run Commands
^^^^^^^^^^^^^^^^^^^

Development tools supported out-of-the-box: (see `docker-compose.override.yml`_)

{% if cookiecutter.framework in ['Symfony', 'TYPO3'] -%}
- composer
- npm
{%- else %}
None yet. Sorry.
{%- endif %}

Source `.envrc`_ to activate natural aliases for those commands:

.. code-block:: console

    . .envrc  # or `source .envrc` in bash

.. note::

    **Optional but recommended:**

    Install and configure `direnv`_ to make this automatic for all projects
    you work on.  See `.envrc`_ for setup instructions.

Alternatively, you can run those commands the classic way, i.e.

.. code-block:: console

    docker-compose run <toolname>

.. _docker-compose.override.yml: docker-compose.override.yml
.. _direnv: https://direnv.net/
.. _.envrc: .envrc

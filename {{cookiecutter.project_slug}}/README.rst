{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Getting Started
---------------

To start developing on this project simply bring up the Docker setup:

.. code-block:: console
{% if cookiecutter.framework in ['Symfony', 'TYPO3'] -%}
    composer install
    docker-compose build
    docker-compose up
{% else -%}
    docker-compose build
    docker-compose up
{%- endif %}

{% if cookiecutter.framework == 'Django' -%}
Migrations will run automatically at startup (via the container entrypoint).
If they fail the very first time simply restart the application.
{%- endif %}

Open your web browser at http://localhost:8000 to see the application
you're developing.  Log output will be displayed in the terminal, as usual.

{% if cookiecutter.container_platform == 'APPUiO' -%}
Initial Setup (APPUiO + GitLab)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{% if cookiecutter.environment_strategy == 'dedicated' -%}
#. Create a *production*, *integration* and *development* project at the
{% else -%}
#. Create a project at the
{%- endif %}
   `VSHN Control Panel <https://control.vshn.net/openshift/projects/appuio%20public>`_.
   For quota sizing consider roughly the sum of ``limits`` of all
   resources (must be strictly greater than the sum of ``requests``):

   .. code-block:: console

        grep -A2 limits deployment/*/*/*yaml
        grep -A2 requests deployment/*/*/*yaml

#. Create a service account as described in the `APPUiO docs
   <https://appuio-community-documentation.readthedocs.io/en/latest/services/webserver/50_pushing_to_appuio.html>`_:

   Create a service account, grant permissions to push images and apply
   configurations, and get the service account's token value:

   .. code-block:: console

{% if cookiecutter.environment_strategy == 'dedicated' -%}
        oc -n {{ cookiecutter.project_slug }}-production create sa gitlab-ci
        oc -n {{ cookiecutter.project_slug }}-production policy add-role-to-user edit -z gitlab-ci
        oc -n {{ cookiecutter.project_slug }}-production sa get-token gitlab-ci
{% else -%}
        oc -n {{ cookiecutter.project_slug }} create sa gitlab-ci
        oc -n {{ cookiecutter.project_slug }} policy add-role-to-user edit -z gitlab-ci
        oc -n {{ cookiecutter.project_slug }} sa get-token gitlab-ci
{%- endif %}

#. Configure the Kubernetes integration in your GitLab project adding
   the ``token`` value from the ``gitlab-ci-token`` secret to:

   -  Operations > Kubernetes > "APPUiO" > Kubernetes cluster details > Service Token

   (*Note:* Make sure "GitLab-managed cluster" is unchecked in the cluster details.)

{% if cookiecutter.environment_strategy == 'dedicated' -%}
#. Grant the service account permissions on the *development* and *integration*
   projects:

   .. code-block:: console

        oc -n {{ cookiecutter.project_slug }}-integration policy add-role-to-user \
          edit system:serviceaccount:{{ cookiecutter.project_slug }}-production:gitlab-ci
        oc -n {{ cookiecutter.project_slug }}-development policy add-role-to-user \
          edit system:serviceaccount:{{ cookiecutter.project_slug }}-production:gitlab-ci
{%- endif %}
{%- endif %}

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

{% if cookiecutter.framework in ['Symfony', 'TYPO3'] -%}
Docker Run Commands
^^^^^^^^^^^^^^^^^^^

Development tools supported out-of-the-box: (see `docker-compose.override.yml`_)

- composer
- npm

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
{%- endif %}

CI/CD Process
^^^^^^^^^^^^^

{% if cookiecutter.environment_strategy == 'dedicated' -%}
We have 3 environments corresponding to 3 namespaces on our container
platform: *development*, *integration*, *production*
{% else -%}
We have 3 environments corresponding to 3 deployments in one namespace on our container
platform: *development*, *integration*, *production*
{%- endif %}

- Any merge request triggers a deployment (of the feature branch) on
  *development*.
- Any change on the main branch, e.g. when a merge request is merged into
  ``master``, triggers a deployment on *integration*.
- To trigger a deployment on *production* push a Git tag, e.g.

  .. code-block:: console

    git checkout master
    git tag 1.0.0
    git push --tags

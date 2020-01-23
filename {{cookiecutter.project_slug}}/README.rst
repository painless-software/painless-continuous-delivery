{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Getting Started
---------------

To start developing on this project simply bring up the Docker setup:

.. code-block:: console
{% if cookiecutter.framework in ['Symfony', 'TYPO3'] %}
    composer install
    docker-compose build
    docker-compose up
{%- else %}
    docker-compose build
    docker-compose up
{%- endif %}
{%- if cookiecutter.framework == 'Django' %}

Migrations will run automatically at startup (via the container entrypoint).
If they fail the very first time simply restart the application.{% endif %}

Open your web browser at http://localhost:8000 to see the application
you're developing.  Log output will be displayed in the terminal, as usual.

For running tests, linting, security checks, etc. see instructions in the
`tests/ <tests/README.rst>`_ folder.

{% if cookiecutter.container_platform == 'APPUiO' -%}
Initial Setup (APPUiO + GitLab)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{% if cookiecutter.environment_strategy == 'dedicated' -%}
#. Create a *production*, *integration* and *development* project at the
{%- else -%}
#. Create a project at the
{%- endif %}
   `VSHN Control Panel <https://control.vshn.net/openshift/projects/appuio%20public>`_.
   For quota sizing consider roughly the sum of ``limits`` of all
   resources (must be strictly greater than the sum of ``requests``):

   .. code-block:: console

        grep -A2 limits deployment/*/*/*yaml
        grep -A2 requests deployment/*/*/*yaml

#. With the commands below, create a service account from your terminal
   (logging in to your cluster first), grant permissions to push images
   and apply configurations, and get the service account's token value:
   (`APPUiO docs <https://appuio-community-documentation.readthedocs.io/en/latest/services/webserver/50_pushing_to_appuio.html>`_)

   .. code-block:: console
{% if cookiecutter.environment_strategy == 'dedicated' %}
        oc -n {{ cookiecutter.project_slug }}-production create sa gitlab-ci
        oc -n {{ cookiecutter.project_slug }}-production policy add-role-to-user admin -z gitlab-ci
        oc -n {{ cookiecutter.project_slug }}-production sa get-token gitlab-ci
{%- else %}
        oc -n {{ cookiecutter.project_slug }} create sa gitlab-ci
        oc -n {{ cookiecutter.project_slug }} policy add-role-to-user admin -z gitlab-ci
        oc -n {{ cookiecutter.project_slug }} sa get-token gitlab-ci
{%- endif %}

#. Use the service account token to configure the
   `Kubernetes integration <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.project_slug }}/-/clusters>`_
   of your GitLab project: (`GitLab docs <https://docs.gitlab.com/ee/user/project/clusters/>`_)

   -  Operations > Kubernetes > "APPUiO" > Kubernetes cluster details > Service Token

   and ensure the following values are set in the cluster details:

   - RBAC-enabled cluster: *(checked)*
   - GitLab-managed cluster: *(unchecked)*
   - Project namespace: {% if cookiecutter.environment_strategy == 'shared' %}"{{ cookiecutter.project_slug }}"{% else %}*(empty)*{% endif %}
{%- if cookiecutter.environment_strategy == 'dedicated' %}

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

{% endif -%}
CI/CD Process
^^^^^^^^^^^^^

{% if cookiecutter.environment_strategy == 'dedicated' -%}
We have 3 environments corresponding to 3 namespaces on our container
platform: *development*, *integration*, *production*
{%- else -%}
We have 3 environments corresponding to 3 deployments in a single namespace
on our container platform: *development*, *integration*, *production*
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

Credits
^^^^^^^

Made with ♥ by Painless Continuous Delivery Cookiecutter. This project was created with:

.. code-block:: console

    cookiecutter gh:painless-software/painless-continuous-delivery \
        project_name="{{ cookiecutter.project_name }}" \
        project_description="{{ cookiecutter.project_description }}" \
        container_platform={{ cookiecutter.container_platform }} \
        container_platform_account="{{ cookiecutter.container_platform_account }}" \
        environment_strategy={{ cookiecutter.environment_strategy }} \
        vcs_platform={{ cookiecutter.vcs_platform }} \
        vcs_account={{ cookiecutter.vcs_account }} \
        framework={{ cookiecutter.framework }} \
        database={{ cookiecutter.database }} \
        license={{ cookiecutter.license }} \
        --no-input

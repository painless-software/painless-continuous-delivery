{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Getting Started
---------------

To start developing on this project simply bring up the Docker setup:

.. code-block:: console
{% if cookiecutter.framework in ['Symfony', 'TYPO3'] %}
    composer install
    docker-compose up
{%- else %}
    docker-compose up
{%- endif %}
{%- if cookiecutter.framework == 'Django' %}

Migrations will run automatically at startup (via the container entrypoint).
If they fail the very first time simply restart the application.{% endif %}

{% set port = ':8080' if cookiecutter.framework == 'SpringBoot' else ':8000' if cookiecutter.framework == 'Django' else ':5000' if cookiecutter.framework == 'Flask' else '' -%}
Open your web browser at http://localhost{{ port }} to see the application
you're developing.  Log output will be displayed in the terminal, as usual.

For running tests, linting, security checks, etc. see instructions in the
`tests/ <tests/README.rst>`_ folder.
{%- if cookiecutter.cloud_platform != '(none)' and cookiecutter.deployment_strategy == 'pipeline' %}

Initial Setup
^^^^^^^^^^^^^

{% if cookiecutter.environment_strategy == 'dedicated' -%}
#. Create a *production*, *integration* and *development* project
{%- else -%}
#. Create a project
{%- endif %}
{%- if cookiecutter.cloud_platform in ['APPUiO'] %}
   at the `VSHN Control Panel <https://control.vshn.net/openshift/projects/appuio%20public>`_.
{%- elif cookiecutter.cloud_platform in ['Rancher'] %} with Rancher.
{%- endif %}
   For quota sizing consider roughly the sum of ``limits`` of all
   resources (must be strictly greater than the sum of ``requests``):

   .. code-block:: console

        grep -A2 limits manifests/*/*/*yaml
        grep -A2 requests manifests/*/*/*yaml
{% if cookiecutter.cloud_platform in ['APPUiO'] %}
#. With the commands below, create a service account from your terminal
   (logging in to your cluster first), grant permissions to push images
   and apply configurations, and get the service account's token value:
   (`APPUiO docs <https://docs.appuio.ch/en/latest/services/webserver/50_pushing_to_appuio.html>`_)

   .. code-block:: console
{% if cookiecutter.environment_strategy == 'dedicated' %}
        oc -n {{ cookiecutter.cloud_project }}-production create sa {{ cookiecutter.automation_user }}
        oc -n {{ cookiecutter.cloud_project }}-production policy add-role-to-user admin -z {{ cookiecutter.automation_user }}
        oc -n {{ cookiecutter.cloud_project }}-production sa get-token {{ cookiecutter.automation_user }}
{%- else %}
        oc -n {{ cookiecutter.cloud_project }} create sa {{ cookiecutter.automation_user }}
        oc -n {{ cookiecutter.cloud_project }} policy add-role-to-user admin -z {{ cookiecutter.automation_user }}
        oc -n {{ cookiecutter.cloud_project }} sa get-token {{ cookiecutter.automation_user }}
{%- endif -%}
{%- elif cookiecutter.cloud_platform in ['Rancher'] %}
#. Create a service account called "{{ cookiecutter.automation_user }}", determine its token.
{%- endif -%}
{%- if cookiecutter.ci_service == 'bitbucket-pipelines.yml' %}

#. Note down service account token and your cluster's URL, and

   - at `Settings > Pipelines > Settings
     <https://bitbucket.org/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/admin/addon/admin/pipelines/settings>`_,
     check "Enable Pipelines",
   - at `Settings > Pipelines > Repository variables
     <https://bitbucket.org/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/admin/addon/admin/pipelines/repository-variables>`_
     configure the following environment variables, which allow the pipeline
     to integrate with your container platform:

     - ``KUBE_TOKEN``
     - ``KUBE_URL``{% if cookiecutter.cloud_platform not in ['APPUiO'] %}
     - ``REGISTRY_PASSWORD`` (for image registry account {{ cookiecutter.registry_user }}){% endif %}

#. Rename the default deployment environments at

   - `Settings > Deployments
     <https://bitbucket.org/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/admin/addon/admin/pipelines/deployment-settings>`_

   as follows:

   - *Test* ➜ *Development*
   - *Staging* ➜ *Integration*
{%- elif cookiecutter.ci_service == '.gitlab-ci.yml' %}

#. Use the service account token to configure the
   `Kubernetes integration <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/clusters>`_
   of your GitLab project: (`GitLab docs <https://docs.gitlab.com/ee/user/project/clusters/>`_)

   - Operations > Kubernetes > "{{ cookiecutter.cloud_platform }}" > Kubernetes cluster details > Service Token

   and ensure the following values are set in the cluster details:

   - RBAC-enabled cluster: *(checked)*
   - GitLab-managed cluster: *(unchecked)*
   - Project namespace: {% if cookiecutter.environment_strategy == 'shared' %}"{{ cookiecutter.cloud_project }}"{% else %}*(empty)*{% endif %}
{%- if cookiecutter.cloud_platform not in ['APPUiO'] %}

#. At `Settings > CI/CD > Variables <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/ci_cd>`__
   add the password for your "{{ cookiecutter.registry_user }}" account to allow the pipeline access your image registry with

   - ``REGISTRY_PASSWORD``
{%- endif %}
{%- endif %}
{%- if cookiecutter.environment_strategy == 'dedicated' %}
{% if cookiecutter.cloud_platform in ['APPUiO'] %}
#. Grant the service account permissions on the *development* and *integration*
   projects:

   .. code-block:: console

        oc -n {{ cookiecutter.cloud_project }}-integration policy add-role-to-user \
          admin system:serviceaccount:{{ cookiecutter.cloud_project }}-production:{{ cookiecutter.automation_user }}
        oc -n {{ cookiecutter.cloud_project }}-development policy add-role-to-user \
          admin system:serviceaccount:{{ cookiecutter.cloud_project }}-production:{{ cookiecutter.automation_user }}
{%- endif %}
{%- endif %}
{%- endif %}

Integrate External Tools
^^^^^^^^^^^^^^^^^^^^^^^^
{% set ns = namespace(external_tools=false) %}
{%- if cookiecutter.monitoring == 'Datadog' and cookiecutter.ci_service == '.gitlab-ci.yml' %}
{%- set ns.external_tools = true %}
:Datadog:
  - Add environment variables ``DATADOG_API_KEY``, ``DATADOG_APP_KEY``, ``DATADOG_APP_NAME`` in
    `Settings > CI/CD > Variables <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/ci_cd>`__
  - Delete secrets in your namespace and run a deployment (to recreate them)
{%- endif %}
{%- if cookiecutter.monitoring == 'NewRelic' and cookiecutter.ci_service == '.gitlab-ci.yml' %}
{%- set ns.external_tools = true %}
:New Relic:
  - Add environment variable ``NEWRELIC_LICENSE_KEY`` in
    `Settings > CI/CD > Variables <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/ci_cd>`__
  - Delete secrets in your namespace and run a deployment (to recreate them)
{%- endif %}
{%- if cookiecutter.monitoring == 'Sentry' and cookiecutter.ci_service == '.gitlab-ci.yml' %}
{%- set ns.external_tools = true %}
:Sentry:
  - Add environment variable ``SENTRY_DSN`` in
    `Settings > CI/CD > Variables <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/ci_cd>`__
  - Delete secrets in your namespace and run a deployment (to recreate them)
  - Configure `Error Tracking <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/error_tracking>`__
    in `Settings > Operations > Error Tracking <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/operations>`__
{%- endif %}
{%- if cookiecutter.docker_registry not in ['(none)', 'registry.appuio.ch', 'registry.gitlab.com'] and cookiecutter.ci_service == '.gitlab-ci.yml' %}
{%- set ns.external_tools = true %}
:Image Registry:
  - Add environment variable ``REGISTRY_PASSWORD`` in
    `Settings > CI/CD > Variables <https://gitlab.com/{{ cookiecutter.vcs_account }}/{{ cookiecutter.vcs_project }}/-/settings/ci_cd>`__
{%- endif %}
{%- if not ns.external_tools %}
Nothing to do here.
{%- endif %}

Working with Docker
^^^^^^^^^^^^^^^^^^^

Create/destroy development environment:

.. code-block:: console

    docker-compose up       # --build to build containers; -d to daemonize
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

{% if cookiecutter.deployment_strategy == 'gitops' -%}
This project only builds and pushes an application image to the image registry.
A separate `GitOps repository`_ handles the deployment of our application,
which will typically roll out our updated image immediately.

.. _GitOps repository: https://{{ cookiecutter.vcs_platform|lower }}/{{ cookiecutter.vcs_account }}/{{ cookiecutter.gitops_project }}

{% set review_tag = 'review-mr<id>' if cookiecutter.ci_service == '.gitlab-ci.yml' else 'review-pr<id>' -%}
- Any merge request automatically builds and pushes a review app image tagged
  ``{{ review_tag }}`` to the image registry.
- Any change on the main branch, e.g. when a merge request is merged into
  ``main``, builds and pushes an image tagged ``latest`` to the image
  registry, which is targeted for use on *integration*.
- To mark an image "ready" for use on *production* push a Git tag on
  the ``main`` branch, e.g.
{%- else -%}
{% if cookiecutter.environment_strategy == 'dedicated' -%}
We have 3 environments corresponding to 3 namespaces on our container
platform: *development*, *integration*, *production*
{%- else -%}
We have 3 environments corresponding to 3 deployments in a single namespace
on our container platform: *development*, *integration*, *production*
{%- endif %}

- Any merge request triggers a deployment of a review app on *development*.
  When a merge request is merged or closed the review app will automatically
  be removed.
- Any change on the main branch, e.g. when a merge request is merged into
  ``main``, triggers a deployment on *integration*.
- To trigger a deployment on *production* push a Git tag, e.g.
{%- endif %}

  .. code-block:: console

    git checkout main
    git tag 1.0.0
    git push --tags

Credits
^^^^^^^

Made with ♥ by `Painless Continuous Delivery`_ Cookiecutter. This project was
generated by:

.. code-block:: console

    cookiecutter gh:painless-software/painless-continuous-delivery \
        project_name="{{ cookiecutter.project_name }}" \
        project_description="{{ cookiecutter.project_description }}" \
        vcs_platform="{{ cookiecutter.vcs_platform }}" \
        vcs_account="{{ cookiecutter.vcs_account }}" \
        vcs_project="{{ cookiecutter.vcs_project }}" \
        ci_service="{{ cookiecutter.ci_service }}" \
        cloud_platform="{{ cookiecutter.cloud_platform }}" \
        cloud_account="{{ cookiecutter.cloud_account }}" \
        cloud_project="{{ cookiecutter.cloud_project }}" \
        environment_strategy="{{ cookiecutter.environment_strategy }}" \
        deployment_strategy="{{ cookiecutter.deployment_strategy }}" \
        gitops_project="{{ cookiecutter.gitops_project }}" \
        docker_registry="{{ cookiecutter.docker_registry }}" \
        registry_user="{{ cookiecutter.registry_user }}" \
        automation_user="{{ cookiecutter.automation_user }}" \
        framework="{{ cookiecutter.framework }}" \
        database="{{ cookiecutter.database }}" \
        cronjobs="{{ cookiecutter.cronjobs }}" \
        checks="{{ cookiecutter.checks }}" \
        tests="{{ cookiecutter.tests }}" \
        monitoring="{{ cookiecutter.monitoring }}" \
        license="{{ cookiecutter.license }}" \
        --no-input

.. _Painless Continuous Delivery: https://github.com/painless-software/painless-continuous-delivery/

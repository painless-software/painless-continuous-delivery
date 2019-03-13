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

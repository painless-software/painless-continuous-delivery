{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Developing
----------

.. code-block:: bash

    docker-compose build    # build the containers
    docker-compose up       # start all containers

Then visit http://localhost to see your application.  Log output will be
displayed in the terminal, as usual.

Working with Docker
^^^^^^^^^^^^^^^^^^^

Create/destroy development environment:

.. code-block:: bash

    docker-compose up -d    # create and start; omit -d to see log output
    docker-compose down     # docker-compose kill && docker-compose rm -af

Start/stop development environment:

.. code-block:: bash

    docker-compose start    # resume after 'stop'
    docker-compose stop     # stop containers, but keep them intact

Other useful commands:

.. code-block:: bash

    docker-compose ps       # list running containers
    docker-compose logs -f  # view (and follow) container logs

See the `docker-compose CLI reference`_ for other commands.

.. _docker-compose CLI reference: https://docs.docker.com/compose/reference/overview/

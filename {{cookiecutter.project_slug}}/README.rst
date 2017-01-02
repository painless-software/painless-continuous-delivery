{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

{{ cookiecutter.project_description }}

Getting Started
---------------

To start developing on this project simply bring up the Docker setup:

.. code-block:: bash
{% if cookiecutter.framework == 'Django' %}
    docker-compose up --build -d
    docker-compose run application python manage.py migrate
    docker-compose logs -f
{% else %}
    docker-compose up --build
{% endif %}
Open your web browser at http://localhost (on a Linux host) or
http://<docker-machine-ip-address> (on OS X and Windows), usually the
IP address of the VirtualBox VM called ``default``, to see the application
you're developing.  Log output will be displayed in the terminal, as usual.

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

Project Configuration
=====================

This folder contains configuration files for running the project as deployed
software, locally for development and on remote hosts.

`application/ <application/>`__
{%- if cookiecutter.framework == 'Django' %}
    Web server to Python interface configuration
{%- endif %}
`database/ <database/>`__
    Database service deployment configuration
`webserver/ <webserver/>`__
    Web server configuration for the project

See Also
--------

Application (framework) specific settings are located in the project's
{% if cookiecutter.framework == 'Django' -%}
``application`` module (see ``application/settings.py``).
{%- else -%}
``application`` module.
{%- endif %}

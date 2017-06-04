============================
Painless Continuous Delivery
============================

|health|

A cookiecutter for projects with continuous delivery baked in.


.. |health| image:: https://landscape.io/github/painless-software/painless-continuous-delivery/master/landscape.svg?style=flat
   :target: https://landscape.io/github/painless-software/painless-continuous-delivery/master
   :alt: Code health

Supported Technologies and Services
===================================

==================== =========================================================
**Languages**        Python (and Python frameworks)
..                   Frontend Web technologies (JavaScript, CSS, Sass/SCSS)
..                   PHP (experimental)
**Version Control**  Git
**Repo Services**    Bitbucket
..                   GitHub
..                   GitLab
**CI Services**      Bitbucket  - |bitbucket|
..                   Codeship   - |codeship|
..                   GitLab CI  - |gitlab-ci|
..                   Shippable  - |shippable|
..                   Travis CI  - |travis-ci|
..                   Vexor CI   - |vexor-ci|
==================== =========================================================


.. |bitbucket| image:: https://img.shields.io/badge/Bitbucket-Pipelines-blue.svg
   :alt: Bitbucket Pipelines
   :target: https://bitbucket.org/painless-software/painless-continuous-delivery/addon/pipelines/home
.. |codeship| image:: https://img.shields.io/codeship/64f85000-617f-0134-d666-52056d8a95f1/master.svg
   :alt: Codeship
   :target: https://app.codeship.com/projects/174831
.. |gitlab-ci| image:: https://gitlab.com/painless-software/painless-continuous-delivery/badges/master/build.svg
   :alt: GitLab CI
   :target: https://gitlab.com/painless-software/painless-continuous-delivery
.. |shippable| image:: https://img.shields.io/shippable/57e164fc6356081000190caa/master.svg
   :alt: Shippable
   :target: https://app.shippable.com/projects/57e164fc6356081000190caa/
.. |travis-ci| image:: https://img.shields.io/travis/painless-software/painless-continuous-delivery/master.svg
   :alt: Travis CI
   :target: https://travis-ci.org/painless-software/painless-continuous-delivery
.. |vexor-ci| image:: https://ci.vexor.io/projects/59719621-2f88-4c7b-95a9-d1536c519e96/status.svg
   :alt: Vexor CI
   :target: https://ci.vexor.io/ui/projects/59719621-2f88-4c7b-95a9-d1536c519e96/builds

Usage
=====

Install `cookiecutter <https://github.com/audreyr/cookiecutter>`_:

.. code-block:: bash

    pip install cookiecutter

Generate a new Cookiecutter template layout:

.. code-block:: bash

    cookiecutter gh:painless-software/painless-continuous-delivery

Under The Hood
==============

The underscore folder, ``{{cookiecutter.project_slug}}/_``, contains files
that are integrated by the post generate hook, ``hooks/post_gen_project.py``,
according to the choices made during the cookiecutter execution.

The ``generators`` folder contains scripts to pre-generate code skeletons
that are integrated manually in this cookiecutter (e.g. framework setups).

Please refer to the README files in those folders for additional details.

Credits
=======

This project is brought to you by `Painless Software`_, a best-practice
consultancy in software development.  Less pain, more fun.


.. _Painless Software: https://painless.software/

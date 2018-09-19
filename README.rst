============================
Painless Continuous Delivery
============================

|about| |health|

A cookiecutter for projects with continuous delivery baked in.


.. |about| image:: https://img.shields.io/badge/About-Painless_Continuous_Delivery-44a0dd.svg
   :target: https://slides.com/bittner/djangocon2017-painless-continuous-delivery/
   :alt: Elevator pitch
.. |health| image:: https://landscape.io/github/painless-software/painless-continuous-delivery/master/landscape.svg?style=flat
   :target: https://landscape.io/github/painless-software/painless-continuous-delivery/master
   :alt: Code health

Supported Technologies and Services
===================================

==================== =========================================================
**Languages**        Python (generic, Django, Flask)
..                   Frontend Web technologies (JavaScript, CSS, Sass/SCSS)
..                   PHP (Symfony, TYPO3, Magento)
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
   :target: https://bitbucket.org/painless-software/painless-continuous-delivery/addon/pipelines/home
   :alt: Bitbucket Pipelines
.. |codeship| image:: https://img.shields.io/codeship/64f85000-617f-0134-d666-52056d8a95f1/master.svg
   :target: https://app.codeship.com/projects/174831
   :alt: Codeship
.. |gitlab-ci| image:: https://gitlab.com/painless-software/painless-continuous-delivery/badges/master/build.svg
   :target: https://gitlab.com/painless-software/painless-continuous-delivery
   :alt: GitLab CI
.. |shippable| image:: https://img.shields.io/shippable/5b3e90d82e388a070068d4bf/master.svg
   :target: https://app.shippable.com/projects/5b3e90d82e388a070068d4bf/
   :alt: Shippable
.. |travis-ci| image:: https://img.shields.io/travis/painless-software/painless-continuous-delivery/master.svg
   :target: https://travis-ci.org/painless-software/painless-continuous-delivery
   :alt: Travis CI
.. |vexor-ci| image:: https://ci.vexor.io/projects/59719621-2f88-4c7b-95a9-d1536c519e96/status.svg
   :target: https://ci.vexor.io/ui/projects/59719621-2f88-4c7b-95a9-d1536c519e96/builds
   :alt: Vexor CI

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

How Can I Contribute?
=====================

See our `contributing guide`_.  Consult our `Wiki`_ for technology notes.

Credits
=======

This project is brought to you by `Painless Software`_, a best-practice
consultancy in software development.  Less pain, more fun.


.. _contributing guide: CONTRIBUTING.rst
.. _Wiki: https://github.com/painless-software/painless-continuous-delivery/wiki
.. _Painless Software: https://painless.software/

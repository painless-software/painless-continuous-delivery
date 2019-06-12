============================
Painless Continuous Delivery
============================

|about| |health|

A cookiecutter for projects with continuous delivery baked in.


.. |about| image:: https://img.shields.io/badge/About-Painless_Continuous_Delivery-44a0dd.svg
   :target: https://slides.com/bittner/djangocon2017-painless-continuous-delivery/
   :alt: Elevator pitch
.. |health| image:: https://img.shields.io/codacy/grade/7aade15697ed4ad39758553efcd31c77/master.svg
   :target: https://www.codacy.com/app/painless/painless-continuous-delivery
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
==================== =========================================================


.. |bitbucket| image:: https://img.shields.io/bitbucket/pipelines/painless-software/painless-continuous-delivery/master.svg
   :target: https://bitbucket.org/painless-software/painless-continuous-delivery/addon/pipelines/home
   :alt: Bitbucket Pipelines
.. |codeship| image:: https://img.shields.io/codeship/64f85000-617f-0134-d666-52056d8a95f1/master.svg
   :target: https://app.codeship.com/projects/174831
   :alt: Codeship
.. |gitlab-ci| image:: https://gitlab.com/painless-software/painless-continuous-delivery/badges/master/build.svg
   :target: https://gitlab.com/painless-software/painless-continuous-delivery/pipelines
   :alt: GitLab CI
.. |shippable| image:: https://img.shields.io/shippable/5b3e90d82e388a070068d4bf/master.svg
   :target: https://app.shippable.com/projects/5b3e90d82e388a070068d4bf/
   :alt: Shippable
.. |travis-ci| image:: https://img.shields.io/travis/painless-software/painless-continuous-delivery/master.svg
   :target: https://travis-ci.org/painless-software/painless-continuous-delivery
   :alt: Travis CI

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

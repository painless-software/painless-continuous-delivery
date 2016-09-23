How To Contribute
=================

If you want to make this piece of software more useful, better fit your needs,
fix bugs or typos your help is greatly appreciated!

- If you have specific changes that should go into the code base please
  prepare a `pull request`_.
- If you're unsure or need to discuss your ideas please open an issue in our
  `bug tracker`_.
- As a general rule, all code changes need to satisfy the default rules
  enforced by `flake8`_ and `PyLint`_ (PEP8 et al.).
- Please add tests and make sure the builds all pass (run ``tox`` locally).
  We recommend using `pyenv`_ to test against all Python version locally.
  Alternatively, you can test only against the versions you already have
  installed on your machine like this, wait for the buld servers to cover the
  missing pieces and fix identified issues with additional commits:

.. code-block:: bash

    tox -e flake8,pylint,py35,py27


.. _pull request: https://github.com/painless-software/painless-continuous-delivery/pulls
.. _bug tracker: https://github.com/painless-software/painless-continuous-delivery/issues
.. _flake8: http://flake8.readthedocs.io/en/latest/
.. _PyLint: https://pylint.org/
.. _pyenv: https://github.com/yyuu/pyenv#basic-github-checkout

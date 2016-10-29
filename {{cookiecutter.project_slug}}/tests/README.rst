Tests
=====

    Software without tests is broken by design.

    -- https://painless.software/writing-tests

Philosophy
----------

No need to install additional packages for running tests
    Add all dependencies for running your tests to ``tests/requirements.txt``.
    (Tox_ will create virtual environments and install those packages
    automagically when running your tests.)


.. _Tox: https://tox.readthedocs.io/en/latest/

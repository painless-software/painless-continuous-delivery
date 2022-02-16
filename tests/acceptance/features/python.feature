Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a Python software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> <database> project checking <checks> and testing <tests>
    When I run the test suite with <commands>
    Then all tests pass successfully

    Examples: Python frameworks
      | framework | database | checks                   | tests       | commands |
      | Django    | Postgres | flake8,pylint,kubernetes | py38,behave | tox      |
      | Flask     | (none)   | flake8,pylint,kubernetes | py38,behave | tox      |

Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a Python software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> project checking <checks> and testing <tests>
    When I run the test suite with <commands>
    Then all tests pass successfully

    Examples: Python frameworks
      | framework | checks        | tests       | commands |
      | Django    | flake8,pylint | py36,behave | tox      |
      | Flask     | flake8,pylint | py36,behave | tox      |

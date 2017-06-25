Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> project with this cookiecutter
    And all the configuration files for the test setup are in place
    When I run the test suite
    Then all tests pass successfully

    Examples: for the following frameworks
      | framework |
      | Django    |
      | Flask     |

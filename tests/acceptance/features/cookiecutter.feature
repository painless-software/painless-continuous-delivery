Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a software developer
  I want to run to run a simple command
  So that I have a working best-practice setup for software development

  Scenario: Default tests pass after project generation
    Given I have just created a project with this cookiecutter
    When I run the test suite
    Then all tests pass successfully

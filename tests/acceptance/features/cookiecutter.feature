Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> project checking <checks> and testing <tests>
    And the test environment has been initialized with <setupcommand>
    And all the configuration files for the test setup are in place
    When I run the test suite with <testsuite>
    Then all tests pass successfully

    Examples: for the following frameworks
      | framework | checks            | tests            | setupcommand     | testsuite                               |
      | Django    | flake8,pylint     | py_local_,behave | true             | tox                                     |
      | Flask     | flake8,pylint     | py_local_,behave | true             | tox                                     |
      | Symfony   | phpcs,twig,jshint | phpunit,jsunit   | composer install | sh -c "composer check && composer test" |

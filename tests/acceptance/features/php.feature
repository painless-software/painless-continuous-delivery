Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> project checking <checks> and testing <tests>
    And system libraries have been installed for developing with PHP
    When I run the test suite with <commands>
    Then all tests pass successfully

    Examples: PHP frameworks
      | framework | checks            | tests          | commands                        |
      | Symfony   | phpcs,twig,jshint | phpunit,jsunit | composer check && composer test |

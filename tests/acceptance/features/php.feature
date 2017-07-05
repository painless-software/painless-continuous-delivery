Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a software developer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  @php
  Scenario Outline: Default tests pass after project generation
    Given I have just created a <framework> project checking <checks> and testing <tests>
    And system libraries have been installed for developing with PHP
    When I run the test suite with <testcommands>
    Then all tests pass successfully

    Examples: PHP frameworks
      | framework | checks            | tests          | testcommands                    |
      | Symfony   | phpcs,twig,jshint | phpunit,jsunit | composer check && composer test |

  @php @docker
  Scenario Outline: Starting to develop is simple and quick
    Given my computer is set up for development with Docker
    And I want to work on a <framework> project
    When I run <buildcommand>
    Then all images are built successfully
    When I run <startcommand>
    Then the project starts up successfully
    And the application is available at <applicationurl>

    Examples: PHP frameworks
      | framework | | buildcommand         | startcommand         | applicationurl   |
      | Symfony   | | docker-compose build | docker-compose up -d | http://localhost |

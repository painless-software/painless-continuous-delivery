Feature: Painless Continuous Delivery project setup powered by Cookiecutter
  As a DevOps engineer
  I want to run just a simple, single command
  So that I get a working best-practice setup for software development

  Scenario: Default tests pass after project generation
    Given I have just created a Django project
    When I generate the deployment manifests
    Then it contains the expected Kubernetes objects

Feature: Customer management

  Background:
    Given the API is available

  Scenario: Create a customer
    Given a valid customer payload
    When the user creates the customer
    Then the API returns the created customer with an ID
    And the customer has a creation timestamp

  Scenario: List customers
    Given customers exist
    When the user lists customers
    Then the API returns all customers ordered by creation date

  Scenario: Get a customer by ID
    Given a customer exists
    When the user requests the customer by ID
    Then the API returns the customer

  Scenario: Missing customer
    Given no customer exists for an ID
    When the user requests the customer by ID
    Then the API returns not found

Feature: Frontend client and ticket UI

  Background:
    Given the API client can reach the backend

  Scenario: View dashboard data
    Given the backend returns customers and tickets
    When the user opens the frontend
    Then customer and ticket lists are shown

  Scenario: Create a customer
    Given the user fills the customer form
    When the user submits the customer form
    Then the customer is created through the API
    And the customer list refreshes

  Scenario: Create a ticket
    Given a customer exists
    When the user fills and submits the ticket form
    Then the ticket is created through the API
    And the ticket list refreshes

  Scenario: Update a ticket status
    Given a ticket exists
    When the user selects a new status
    Then the ticket status is updated through the API

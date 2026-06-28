Feature: Ticket management

  Background:
    Given an existing customer

  Scenario: Create a ticket for a customer
    Given a valid ticket payload
    When the user creates the ticket
    Then the API returns the created ticket with status "Pendiente"
    And the ticket is associated with the customer

  Scenario: Reject a ticket for a missing customer
    Given no customer exists for the ticket client ID
    When the user creates the ticket
    Then the API returns not found

  Scenario: List tickets
    Given tickets exist
    When the user lists tickets
    Then the API returns all tickets ordered by creation date

  Scenario: Update ticket status
    Given a ticket exists
    When the user updates the status to "En progreso"
    Then the API returns the ticket with status "En progreso"

  Scenario: Reject invalid ticket status
    Given a ticket exists
    When the user updates the status to an unsupported value
    Then the API returns a validation error

Feature: Ticket audit events

  Background:
    Given audit storage is available

  Scenario: Audit ticket creation
    Given an existing customer
    When the user creates a ticket with header "X-User" set to "agent@example.com"
    Then an audit event records action "ticket_created"
    And the audit event includes the acting user and ticket ID

  Scenario: Audit status changes
    Given a ticket exists
    When the user changes the ticket status
    Then an audit event records action "ticket_status_updated"
    And the audit event includes the previous and new statuses

  Scenario: Default audit user
    Given a ticket exists
    When the user changes the ticket status without an audit header
    Then the audit event user is "system"

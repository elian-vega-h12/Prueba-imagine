Feature: Salesforce integration document

  Scenario: Explain Salesforce integration
    Given the reviewer opens "salesforce.md"
    When they read the proposal
    Then it describes Salesforce objects to use
    And it describes synchronized information
    And it includes Apex Trigger and LWC examples
    And it explains Experience Cloud exposure

# Salesforce Integration Proposal

I would integrate Salesforce as the customer support visibility layer for the ticket system. The relational application remains the operational source for ticket creation and status updates, while Salesforce receives synchronized customer and ticket records for CRM workflows, reporting, and external self-service.

## Salesforce Objects

- `Account`: stores the customer's company.
- `Contact`: stores the customer's name and email.
- `Case`: represents each support ticket, linked to the related `Account` and `Contact`.
- `Support_Audit__c`: custom object for important lifecycle events such as ticket creation and status changes.

## Data To Synchronize

The application would sync client `name`, `email`, and `company` into `Contact` and `Account`. Ticket `title`, `description`, `status`, `created_at`, and the local ticket ID would sync into `Case`. Audit events would sync into `Support_Audit__c` with the acting user, action, ticket identifier, and event timestamp.

## Apex Trigger Example

```apex
trigger CaseStatusAuditTrigger on Case (after update) {
    List<Support_Audit__c> audits = new List<Support_Audit__c>();

    for (Case currentCase : Trigger.new) {
        Case previousCase = Trigger.oldMap.get(currentCase.Id);
        if (currentCase.Status != previousCase.Status) {
            audits.add(new Support_Audit__c(
                Case__c = currentCase.Id,
                Action__c = 'Status changed to ' + currentCase.Status,
                User__c = UserInfo.getUserName(),
                Event_Date__c = System.now()
            ));
        }
    }

    if (!audits.isEmpty()) {
        insert audits;
    }
}
```

## LWC Example

```js
import { LightningElement, api, wire } from 'lwc';
import getCases from '@salesforce/apex/SupportTicketController.getCases';

export default class SupportTicketList extends LightningElement {
  @api contactId;

  columns = [
    { label: 'Subject', fieldName: 'Subject' },
    { label: 'Status', fieldName: 'Status' },
    { label: 'Created', fieldName: 'CreatedDate', type: 'date' }
  ];

  @wire(getCases, { contactId: '$contactId' })
  cases;
}
```

## Experience Cloud

I would expose a customer portal in Experience Cloud where authenticated customers can view their Cases, create new support requests, and track status changes. Access would be controlled with sharing rules and Experience Cloud profiles so each customer only sees records linked to their own Contact or Account.

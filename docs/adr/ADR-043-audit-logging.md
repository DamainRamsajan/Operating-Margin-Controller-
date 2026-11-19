# ADR-043: Administrative audit logging

- **Status:** Proposed (implemented in the console)
- **Context:** Customers and auditors need to see who accessed or changed what, without case content, and be able to detect tampering.
- **Decision:** A hash-chained, exportable audit log of authentication failures, denied access, evidence views, downloads, label submissions and audit exports, with an offline verifier; ship it to the customer's log platform and anchor the head hash externally.
- **Consequences:** Tamper evidence and exportability; volume and retention need to be managed; the file-based log moves into the database in WS2.

# Pilot readiness program

Date: 5 November 2026. Replaces the earlier "pilot kit" wording. Decision (founder, 5 November 2026): no local, MVP or prototype work; build a production-grade product that is ready for a professional pilot with real customers.

## 1. Where we honestly are

The core is real and tested: certified audits, signed statements, a standalone verifier, a read-only console, and (as of this drop) production-shaped signing, access control, security headers, health checks, an audit log, structured logs, hash-pinned dependencies, an SBOM, and a clean static and dependency scan. **It is not pilot-ready.** The checklist (`READINESS-CHECKLIST.csv`, 91 items) shows 17 of 62 priority-0 items done (about 38 percent weighted). Run `python scripts/readiness_report.py` for the live number.

| Area | Exists and is tested | Missing for a real pilot |
|---|---|---|
| Statistics and evidence | Audits, parity, stationarity warning, COSE statements (Ed25519, ES256), verifier, vectors | Independent statistical review; validation on real customer data |
| Console | Home, verdict, evidence, setup, review; roles; CSP; audit log | Database persistence, async jobs, real connectors, alerts, share links, auditor portal |
| Identity | Authenticating-proxy mode with shared secret and group-to-role mapping | Verification against a real identity provider; native OIDC; service accounts |
| Keys | Signer abstraction, ES256 | KMS adapter for the pilot's cloud; rotation procedure |
| Operations | Health and readiness, JSON logs, Dockerfile, compose reference | Verified deployment on real infrastructure, Helm or Terraform, backups and a restore drill, observability, runbooks that have been exercised |
| Assurance | Threat model v0, static scan, dependency audit | Penetration test, accessibility audit, DAST, fuzzing, counsel review (EU Cyber Resilience Act scope, AI Act role) |
| Commercial | Contract and offer drafts | Signed agreements, pilot SLA, support process |

## 2. Definition of pilot-ready (Gate P)

All priority-0 items in the checklist are done and the following are true:
1. A customer's IdP logs users in through the production path; roles work; every access is in a verifiable audit log.
2. Data lives in PostgreSQL and object storage inside the customer's tenant; a restore from backup has been demonstrated.
3. Statements are signed with a KMS-held key in the customer's cloud; the public verifier validates them.
4. The deployment has been built, signed, scanned and run on real infrastructure; upgrade and rollback have been rehearsed.
5. One real connector for the partner's helpdesk works on their pseudonymized data.
6. A third-party penetration test has no open high findings; an independent statistician has reviewed the methods; accessibility and load tests pass.
7. Contracts, SLA, support and incident communication are in place; counsel has confirmed our obligations under the EU Cyber Resilience Act and the AI Act.

## 3. Principles
Customer-tenant deployment (their cloud, their data, their keys). Read-only first. Independence and no contingent fees. Nothing is called done without evidence in the repository. Anything untested is labeled untested.

## 4. Workstreams

| WS | Scope | Exit criteria |
|---|---|---|
| WS1 Identity and access | Proxy SSO (done), real IdP verification, native OIDC, service accounts, SCIM later | Verified with a real IdP; roles tested end to end |
| WS2 Data layer | PostgreSQL with migrations, object storage, encryption at rest, backup and restore, retention and deletion | Restore drill passed; retention jobs tested |
| WS3 Keys and evidence | KMS signers, rotation, transparency registration, timestamping, public verifier release | Pilot-cloud KMS signer in use; rotation rehearsed |
| WS4 Application hardening | Headers (done), input limits, rate limits, fuzzing, DAST | DAST clean; fuzzers run in CI |
| WS5 Supply chain | Locks and SBOM (done), signed images, image scan, disclosure policy, CRA runbook | Signed, scanned image and SBOM attached to a release |
| WS6 Deployment and operations | Image, Helm or Terraform, network policy, observability, SLOs, upgrade and rollback, runbooks, DR drill | Real deployment verified; drill passed |
| WS7 Product completeness | Real connector, async jobs, billing estimator, human-access checks, share links, alerts | Partner's data audited end to end |
| WS8 Quality | Unit and integration (done), browser tests, load, accessibility, statistical review, usability study | All pass with budgets met |
| WS9 Security assurance | Threat model, pen test, questionnaires, security pack, SOC 2 decision, insurance | Pen test passed; pack current |
| WS10 Legal and commercial | Agreements, DPA, subprocessors, SLA, counsel review | Signed with the partner |
| WS11 Pilot operations | Onboarding playbook, support, incident comms, success criteria | Playbook rehearsed |
| WS12 Documentation | Architecture (done), admin guide, API reference, data dictionary | Reviewed by someone who did not write it |

## 5. The sequence

| Step | What | Who | Exit |
|---|---|---|---|
| 1 | Decide environment, IdP, cloud for keys, pen-test vendor, SOC 2 timing (D16 to D21 below) | Founder | Decisions recorded |
| 2 | Data layer: PostgreSQL and migrations, object storage, port console and gate, backup and restore scripts | Me | Tests on PostgreSQL in CI; restore script tested |
| 3 | KMS signer adapter for the chosen cloud, rotation procedure | Me, founder for a cloud account | Signing with a KMS-held key demonstrated |
| 4 | Async job runner, ingestion limits, CSV hardening, rate limiting | Me | Large-file and abuse tests pass |
| 5 | First real connector against the partner's helpdesk | Me with the partner | Their pseudonymized data audited |
| 6 | Real deployment: build and sign the image in CI, Helm or Terraform, IdP login, observability, runbooks, restore and rollback drills | Me and founder | Checklist WS6 P0 done |
| 7 | Quality gates: browser tests, load tests, accessibility, fuzzing, DAST | Me | All green in CI |
| 8 | Independent reviews: statistician, penetration test, counsel (CRA scope, AI Act role) | Third parties | Reports received; no open high findings |
| 9 | Pilot features: billing estimator, human-access checks, evidence versioning and share links, alerts | Me | Checklist WS7 P0 done |
| 10 | Pilot operations: SLA, support process, incident communication, security pack, contracts | Founder and me | Signed and rehearsed |
| 11 | Go or no-go review with the readiness report | Founder | `gate_p_ready` is true |
| 12 | Start the pilot; weekly review of defects, incidents and success criteria | Both | First verified statement in the partner's hands |

## 6. Decisions needed from you
| ID | Decision | My recommendation |
|---|---|---|
| D16 | Target environment for the first pilot (AWS, Azure, GCP, or the partner's own Kubernetes) | Match the first design partner; build cloud-neutral and add one KMS adapter |
| D17 | Identity provider for pilots | Support any OIDC provider through the authenticating proxy first |
| D18 | Database and storage | PostgreSQL and S3-compatible object storage |
| D19 | Penetration-test vendor and budget; book 4 to 6 weeks ahead of go-live | Boutique firm with API and web experience |
| D20 | SOC 2 Type I timing | Decide after two partners; use the security pack until then |
| D21 | Who has authority to approve go-live | You |

## 7. What only people can do, and lead times
Penetration test (4 to 6 weeks), counsel review (2 to 4 weeks), independent statistical review (2 to 4 weeks), accessibility expert audit (2 weeks), a real cloud account and identity provider for verification, signing contracts. These run in parallel with the build, which is why booking them early matters.

## 8. Indicative timeline (an estimate, not a promise)
With a design partner signed by mid-December and the decisions above made this week, Gate P is plausible between mid-February and mid-March 2027. It slips one-for-one if the partner or third-party reviews slip.

## 9. Risks to the plan
Scope creep into features before the P0 base is done; third-party lead times; the partner's environment differing from our reference; discovering in review that the statistics need changes; EU Cyber Resilience Act obligations applying to customer-deployed software sooner than expected (counsel to confirm) [V].

## 10. Sources for these requirements
EU Cyber Resilience Act timeline and scope summaries (vulnerability and incident reporting duties from 11 September 2026, SBOM duties from December 2027, customer-deployed software likely in scope, pure SaaS likely out) [V]; enterprise security-review checklists (SSO and SCIM, role-based access, exportable audit logs, key management, SBOM, penetration-test summary, questionnaires such as CAIQ-Lite and SIG) [V]. See arc42 Appendix C.

# ADR-028: Interoperate with developer tools

- **Status:** Proposed
- **Context:** Replay, shadow reports, upgrade pull requests and CI gates are shipping in open-source and commercial developer tools, many free; none was reported to sign promotion verdicts or give anytime-valid certified results [S39][V].
- **Decision:** Do not build general-purpose replay or evaluation runners. Provide import adapters for Langfuse, LangSmith, Braintrust, Kitaru and similar exports, and a CI promotion gate that returns a signed verdict registered in the transparency service.
- **Consequences:** Faster adoption and less build; dependence on third-party export formats; differentiation rests on certified statistics, business parity, independence and signed evidence.

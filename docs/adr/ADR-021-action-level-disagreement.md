# ADR-021: Action-level disagreement for generative agents

- **Status:** Proposed (pending spike S-b)
- **Context:** Certified audits need an observable disagreement signal and a prediction-determined loss; free-text answers provide neither.
- **Decision:** Define disagreement over consequential decisions and actions (resolve or escalate, category, tool calls, refunds, compliance flags). A versioned, audited material-difference classifier decides whether two free-text answers differ materially. Residual free-text quality is measured with prediction-powered inference and graded E2.
- **Consequences:** Extends audits to support agents at a bounded loss of theoretical guarantee; classifier errors cost label efficiency and are reported; scope limits are stated in every certificate.

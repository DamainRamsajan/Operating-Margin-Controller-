# ADR-033: Server-rendered UI first

- **Status:** Accepted (29 October 2026, founder decision D13; implemented in milestone M1)
- **Context:** The product ships into customer tenants; the pilot kit must install in a day; the needed visuals (decision card, dot grid, trajectory) are plain SVG and the prototype shows they work without a framework.
- **Decision:** Build the console as server-rendered pages (FastAPI and Jinja; HTMX only if interaction needs it) with SVG charts in the same container as the engine; defer a single-page app until interaction needs it.
- **Consequences:** Small attack surface, accessible by default, easy deployment; less rich client interaction; revisit after usability tests.

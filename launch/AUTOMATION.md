# What is automated, how, and what stays with you

| Task | Tool | State |
|---|---|---|
| Tests, lint, vector checks | GitHub Actions in both repos | Already in the code |
| Verifier releases to PyPI | GitHub Actions with PyPI trusted publishing (no stored token) | One-time setup below |
| Website | `site/` on Cloudflare Pages (free) | Upload or connect the repo |
| Outreach drafts and meeting slots | Gmail and Google Calendar connectors in Claude | You connect; I draft; you send |
| Contracts and signatures | Common Paper | You send; templates are standard |
| Pipeline and weekly metrics | `launch/pipeline.csv` and `scripts/pipeline_report.py` | Ready |
| Target list, content drafts, discovery prep | Me, from public information | Each round |

## One-time setup
**Site on Cloudflare Pages.** Dashboard, Workers and Pages, Create, Pages, Upload assets, drag the `site/` folder. Or connect the private repo and set the build output directory to `site` (no build command). Then set the contact address: `sed -i 's/CONTACT_EMAIL/you@yourdomain.com/g' site/index.html`.

**PyPI release for `omc-verify`.** On pypi.org, Your projects, Publishing, add a pending trusted publisher: owner `DamainRamsajan`, repository `omc-verify`, workflow `release.yml`, environment `pypi`. Then: `git tag v0.1.0 && git push origin v0.1.0`. The name `omc-verify` was free when checked on 28 October 2026.

## Stays with you (cannot or should not be automated)
Sending outreach (compliance and relationships), signing contracts, entity and bank setup, accepting or declining partners, and any statement made publicly under your name.

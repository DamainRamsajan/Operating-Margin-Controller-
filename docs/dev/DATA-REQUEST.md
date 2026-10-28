# Data request: what we need, why, and how to get it safely

## 1. What we need, in priority order

| Priority | Data | Used for | Minimum useful size |
|---|---|---|---|
| A | Decisions from **two model versions on the same cases**, plus **gold labels** for a sample (spike S-a) | Does the certified audit work on real LLM support decisions? How many labels does it need? | 5,000 cases; at least 200 disagreements with a gold label |
| B | **Column headers only** of the helpdesk and AI-vendor exports (spike S-e) | Which connectors are feasible | Headers and field descriptions, no rows |
| C | A vendor **resolution and billing export** (pseudonymized) (spike S-c) | Outcome billing audit | 500 rows |
| D | **Human-request and disclosure event timestamps** (spike S-j) | Human-access compliance audit | 1,000 requests |
| E | The **refund, credit and discount policy** document (spike S-g) | Authority rules | The document; contains no personal data |

Only A is needed to continue the core work. B to E can follow.

## 2. Three ways to get A this week (pick one)

### Path 1: no partner, you run it (1 to 2 hours, small API cost)
Real LLMs on public data. The public banking support dataset is downloaded automatically.

```bash
export ANTHROPIC_API_KEY=...      # or: export OPENAI_API_KEY=...
python scripts/llm_pair_spike.py --provider anthropic --incumbent-model MODEL_A --candidate-model MODEL_B --n 20     # dry run
python scripts/llm_pair_spike.py --provider anthropic --incumbent-model MODEL_A --candidate-model MODEL_B --n 2000
omc check-data --incumbent data/llm_pair/incumbent.csv --candidate data/llm_pair/candidate.csv --labels data/llm_pair/gold.csv
omc keygen --out-dir keys
omc gate --incumbent data/llm_pair/incumbent.csv --candidate data/llm_pair/candidate.csv --labels data/llm_pair/gold.csv --key keys/omc-key.pem --out-dir out/llm_gate
```

Use two real model versions you have access to (for example an older and a newer one). The script was written without API access and is untested; if the dry run fails, send me the error. Then send me the JSON printed by `check-data` and `gate` (aggregate numbers only).

### Path 2: a friendly support team (best evidence, needs one person with export rights)
Ask for a 30-day export from an AI support tool that has run two model versions or a vendor change. A plain-prose ask you can adapt:

> I am building a tool that tells a support team, with statistical proof, whether swapping an AI model or vendor made answers worse, using as few human labels as possible. I would like to test it on a 30-day export of your AI support decisions, with case IDs replaced by random codes and no message text, names or emails. It is read-only on your side, runs in my own environment, and I will share the results with you. Would one of your analysts have 30 minutes to export it?

What they export (CSV, no free text): `case_id, ts, prediction` for each model version, and `case_id, gold` for any cases a human reviewed.

### Path 3: your own company data
If Intellica or a client already runs an AI support or classification workflow, the same three files apply.

## 3. Safe handling checklist
1. **No free text, names, emails, phone numbers or account numbers.** Decisions and labels only.
2. **Pseudonymize ids before they leave the owner:**
   ```bash
   echo "choose-a-long-random-secret-and-keep-it" > secret.txt
   omc pseudonymize --in incumbent.csv --out incumbent_p.csv --column case_id --secret-file secret.txt
   ```
   Use the same secret file for every file so ids still match. Never share the secret.
3. **Check before sharing:** `omc check-data --incumbent ... --candidate ... --labels ...` prints counts and rates only.
4. **Send me only aggregates** (the `check-data` and `gate` output) unless the owner has approved sharing the files. Do not paste raw rows into this chat.
5. If the data covers EU residents, the owner's privacy lead should approve the purpose (evaluation of model changes) first.

## 4. Templates
`data/templates/` has example headers: `predictions_template.csv`, `gold_template.csv`, `decisions_template.csv`, `tickets_template.csv`.

## 5. Other public datasets worth trying next (check each licence before redistributing)
| Dataset | Why | Note |
|---|---|---|
| Banking77 (used in S-a-lite) | Real banking support intents | Single-label classification |
| CLINC150 | Many intents plus out-of-scope queries | Tests the "no matching intent" decision |
| ABCD (Action-Based Conversations Dataset) | Real agent workflows with actions, closer to support agents | Needs conversion to action-level decisions |
| MultiWOZ | Multi-domain task dialogs | Less like support tickets |

## 6. Helpdesk export checklist (to confirm in spike S-e, per platform)
Look for: a stable case id; created, first-response and solved timestamps; reopen events; customer satisfaction score; channel; tags or custom fields that mark AI involvement; vendor resolution state (confirmed or assumed); refund or credit actions with amounts; human-request and escalation events. Field names differ by platform and plan, so list what each tool actually exposes (headers only) and send me that list.

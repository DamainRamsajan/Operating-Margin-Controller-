# Codespaces: upload and first run

## 1. Open the repo in a Codespace
GitHub repo page, green **Code** button, **Codespaces** tab, **Create codespace on main**.
The dev container installs everything and runs the tests automatically (about two minutes).

## 2. Upload the zip
Drag `omc-repo-m0-full.zip` into the file Explorer (left panel) of the Codespace. Then in the terminal (Ctrl+backtick):

```bash
unzip -o omc-repo-m0-full.zip -d /tmp/omc && cp -r /tmp/omc/omc/. . && rm -rf /tmp/omc omc-repo-m0-full.zip
git add -A && git commit -m "M0: code scaffold, tests, dev container, ADR-031 and 032" && git push origin main
```

If you only want the code (you already uploaded the docs), use `omc-code-m0-only.zip` the same way.
The zips contain a top-level `omc/` folder, which is why the `cp` line copies from `/tmp/omc/omc/.`.

Later drops use the same two commands with the new zip name.

## 3. Check it works (inside the Codespace terminal)

```bash
pip install -e ".[dev,spike]"
python scripts/make_vectors.py
pytest -q                 # 25 fast tests
pytest -q -m slow         # 3 statistical simulations
python scripts/demo.py    # end-to-end demo (about 15 seconds)
```

Expected demo: `benign` is promoted (tier 0, exit 0), `regression` is rejected (tier 1, exit 20), `unclear` is held (exit 10), statements and chains verify, the exposure table shows a critical retirement.

## 4. Everyday commands

```bash
omc keygen --out-dir keys                       # signing key (never commit *.pem)
omc sample --out-dir data/sample --n 30000      # synthetic data
omc gate --incumbent data/sample/benign/incumbent.csv --candidate data/sample/benign/candidate.csv \
         --labels data/sample/benign/gold.csv --key keys/omc-key.pem --out-dir out/gate
omc-verify statement out/gate/verdict.cose --pubkey keys/omc-key.pub.pem
omc exposure --decisions data/sample/ops/decisions.csv --deprecations data/sample/ops/deprecations.json --as-of 2026-10-27
omc leaks --tickets data/sample/ops/tickets.csv
omc redact --in data/sample/ops/transcripts.txt --out out/redacted.txt
omc leakage-audit --reviewed 300 --leaks 0 --limit 0.02
```

Gate exit codes: `0` promote, `10` hold (more traffic or labels needed), `20` reject.

## 5. If something fails
- `omc: command not found`: run `pip install -e ".[dev,spike]"` again.
- Tests fail after a Python upgrade: the dev container pins Python 3.12; rebuild the container (Command Palette, Codespaces: Rebuild Container).
- Never commit private keys. `.gitignore` excludes `*.pem` except the public test vectors.

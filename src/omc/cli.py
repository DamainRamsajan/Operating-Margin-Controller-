"""omc command line (milestone M0). See docs/dev/CODESPACES.md."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="omc", description="Operating-Margin Controller (M0)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    k = sub.add_parser("keygen", help="create a development signing key pair (production keys belong in a KMS)"); k.add_argument("--out-dir", default="keys"); k.add_argument("--alg", choices=["ed25519", "es256"], default="ed25519")
    s = sub.add_parser("sample", help="write synthetic sample data"); s.add_argument("--out-dir", default="data/sample")
    s.add_argument("--n", type=int, default=30000)

    g = sub.add_parser("gate", help="CI promotion gate: certified paired audit with a signed verdict")
    g.add_argument("--incumbent", required=True); g.add_argument("--candidate", required=True)
    g.add_argument("--labels"); g.add_argument("--key", required=True); g.add_argument("--out-dir", default="out/gate")
    g.add_argument("--epsilon", type=float, default=0.01); g.add_argument("--alpha", type=float, default=0.05)
    g.add_argument("--label-rate", type=float, default=0.5); g.add_argument("--workflow", default="support")
    g.add_argument("--markdown", action="store_true", help="print the pull-request comment instead of JSON")
    g.add_argument("--incumbent-name", default="incumbent"); g.add_argument("--candidate-name", default="candidate")

    e = sub.add_parser("exposure", help="model exposure inventory and retirement calendar")
    e.add_argument("--decisions", required=True); e.add_argument("--deprecations", required=True)
    e.add_argument("--as-of", default=date.today().isoformat()); e.add_argument("--json", action="store_true")

    lk = sub.add_parser("leaks", help="cost per accepted outcome and ranked leaks"); lk.add_argument("--tickets", required=True)

    r = sub.add_parser("redact", help="redact common personal data patterns")
    r.add_argument("--in", dest="inp", required=True); r.add_argument("--out", required=True)
    a = sub.add_parser("leakage-audit", help="bound residual leakage from a reviewed sample")
    a.add_argument("--reviewed", type=int, required=True); a.add_argument("--leaks", type=int, required=True)
    a.add_argument("--limit", type=float, default=0.01); a.add_argument("--alpha", type=float, default=0.05)
    t = sub.add_parser("provider-terms", help="check provider data-use terms against a policy")
    t.add_argument("--terms", required=True); t.add_argument("--policy", required=True)

    cn = sub.add_parser("console", help="serve the read-only console for a workspace (local use)")
    cn.add_argument("--workspace", required=True); cn.add_argument("--host", default="127.0.0.1"); cn.add_argument("--port", type=int, default=8000)
    cn.add_argument("--auth-mode", choices=["none", "proxy"], default=os.environ.get("OMC_AUTH_MODE", "none"))
    cn.add_argument("--hsts", action="store_true"); cn.add_argument("--allow-insecure-bind", action="store_true")
    av = sub.add_parser("audit-verify", help="verify the integrity of an administrative audit log"); av.add_argument("file")
    dw = sub.add_parser("demo-workspace", help="build a demo workspace for the console")
    dw.add_argument("--out", default="demo-workspace"); dw.add_argument("--n", type=int, default=30000)
    cd = sub.add_parser("check-data", help="readiness check for gate input files (prints aggregates only)")
    cd.add_argument("--incumbent", required=True); cd.add_argument("--candidate", required=True); cd.add_argument("--labels"); cd.add_argument("--out")
    ps = sub.add_parser("pseudonymize", help="replace an id column with a keyed hash before sharing")
    ps.add_argument("--in", dest="inp", required=True); ps.add_argument("--out", required=True)
    ps.add_argument("--column", default="case_id"); ps.add_argument("--secret-file", required=True)

    v = sub.add_parser("verify", help="verify a signed statement or a chain (same as omc-verify)")
    v.add_argument("kind", choices=["statement", "chain"]); v.add_argument("file"); v.add_argument("--pubkey", required=True)

    x = ap.parse_args(argv)

    if x.cmd == "keygen":
        from omc.vault.statement import generate_keypair
        priv, pub = generate_keypair(x.out_dir, alg=x.alg); print(f"wrote {priv} and {pub}"); return 0
    if x.cmd == "sample":
        from omc.sample import SCENARIOS, make_ops_data, make_scenario
        for sc in SCENARIOS:
            print(json.dumps(make_scenario(Path(x.out_dir) / sc, sc, n=x.n)))
        make_ops_data(Path(x.out_dir) / "ops"); return 0
    if x.cmd == "gate":
        from omc.audit.gate import run_gate
        code, payload = run_gate(x.incumbent, x.candidate, x.labels, x.key, x.out_dir, epsilon=x.epsilon,
                                 alpha=x.alpha, label_rate=x.label_rate, workflow=x.workflow,
                                 incumbent_name=x.incumbent_name, candidate_name=x.candidate_name)
        if x.markdown:
            from omc.render import to_markdown
            print(to_markdown(payload)); return code
        print(json.dumps({k: payload[k] for k in ("verdict", "tier", "reason", "grade", "n_cases", "n_disagree",
                                                   "n_labeled", "stopping_index", "rho_ub", "delta_ub", "delta_lb")}, indent=2))
        return code
    if x.cmd == "exposure":
        from omc.exposure.inventory import build_inventory, to_markdown
        from omc.ingest.csv_adapter import read_decisions, read_retirements
        as_of = date.fromisoformat(x.as_of)
        rows = build_inventory(read_decisions(x.decisions), read_retirements(x.deprecations), as_of)
        print(json.dumps(rows, indent=2) if x.json else to_markdown(rows, as_of)); return 0
    if x.cmd == "leaks":
        from omc.report.leaks import leak_report
        print(json.dumps(leak_report(x.tickets), indent=2)); return 0
    if x.cmd == "redact":
        from omc.privacy.gate import redact
        text, counts = redact(Path(x.inp).read_text()); Path(x.out).write_text(text); print(json.dumps(counts)); return 0
    if x.cmd == "leakage-audit":
        from omc.privacy.gate import leakage_audit
        res = leakage_audit(x.reviewed, x.leaks, x.limit, x.alpha); print(json.dumps(res, indent=2))
        return 0 if res["decision"] == "release" else 20
    if x.cmd == "provider-terms":
        from omc.privacy.gate import check_provider_terms
        fails = check_provider_terms(json.load(open(x.terms)), json.load(open(x.policy)))
        print(json.dumps({"pass": not fails, "failures": fails})); return 0 if not fails else 20
    if x.cmd == "demo-workspace":
        from omc.console.demo import build_workspace
        build_workspace(x.out, n=x.n); print(f"workspace ready: {x.out}  (run: omc console --workspace {x.out})"); return 0
    if x.cmd == "console":
        import uvicorn

        from omc.console.app import create_app
        from omc.console.security import check_bind_safety
        check_bind_safety(x.host, x.auth_mode, x.allow_insecure_bind)
        secret = os.environ.get("OMC_PROXY_SECRET")
        gmap = json.loads(os.environ["OMC_GROUP_MAP"]) if os.environ.get("OMC_GROUP_MAP") else None
        if x.auth_mode == "proxy" and not secret:
            sys.exit("proxy mode needs OMC_PROXY_SECRET (a long random value shared with your authenticating proxy)")
        print(f"OMC console on http://{x.host}:{x.port} (auth: {x.auth_mode})")
        uvicorn.run(create_app(x.workspace, auth_mode=x.auth_mode, proxy_secret=secret, group_map=gmap, hsts=x.hsts),
                    host=x.host, port=x.port, log_level="warning"); return 0
    if x.cmd == "audit-verify":
        from omc.console.audit import verify_file
        ok, msg = verify_file(x.file); print(json.dumps({"valid": ok, "detail": msg})); return 0 if ok else 1
    if x.cmd == "check-data":
        from omc.ingest.check import check_gate_inputs
        res = check_gate_inputs(x.incumbent, x.candidate, x.labels); print(json.dumps(res, indent=2))
        if x.out:
            Path(x.out).write_text(json.dumps(res, indent=2))
        return 0 if not [i for i in res["issues"] if "no ts column" not in i] else 20
    if x.cmd == "pseudonymize":
        from omc.ingest.check import pseudonymize_column
        n = pseudonymize_column(x.inp, x.out, x.column, Path(x.secret_file).read_bytes().strip())
        print(json.dumps({"rows": n, "column": x.column})); return 0
    if x.cmd == "verify":
        from omc_verify.__main__ import main as vmain
        return vmain([x.kind, x.file, "--pubkey", x.pubkey])
    return 2


if __name__ == "__main__":
    sys.exit(main())

"""OMC console (ADR-033): server-rendered, read-only except for review labels (D13 to D15).

Workspace layout (created by `omc gate --out-dir WS/gates/NAME` and `omc demo-workspace`):
  WS/gates/NAME/{verdict.cose, verdict.json, verdict.md, chain.jsonl, trajectory.json, review_queue.csv}
  WS/keys/omc-key.pub.pem        public key used to verify statements
  WS/exposure.json               optional: output of `omc exposure --json`
  WS/readiness.json              optional: output of `omc check-data`
Local use only in this release: it binds to 127.0.0.1 by default and has no login yet.
"""
from __future__ import annotations

import csv
import json
import os
import re
import secrets
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from omc.console import charts
from omc.console.audit import AuditLog
from omc.console.security import (
    DEFAULT_GROUP_MAP,
    ROLE_RANK,
    get_logger,
    new_nonce,
    required_role,
    resolve_role,
    security_headers,
)
from omc.render import headline, per_1000
from omc.vault import chain
from omc.vault.statement import load_public_key, verify_statement

NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")
FILES = {"verdict.cose", "verdict.json", "verdict.md", "chain.jsonl", "trajectory.json"}
CHIP = {"PROMOTE": "ok", "REJECT": "bad", "HOLD": "warn"}
BATCH = 25


def create_app(workspace, auth_mode: str = "none", proxy_secret: str | None = None, group_map: dict | None = None,
               hsts: bool = False) -> FastAPI:
    if auth_mode not in ("none", "proxy"):
        raise ValueError("auth_mode must be none or proxy")
    if auth_mode == "proxy" and not proxy_secret:
        raise ValueError("proxy mode needs a proxy secret")
    ws = Path(workspace).resolve()
    gmap = group_map or DEFAULT_GROUP_MAP
    audit_log = AuditLog(ws / "audit" / "admin-audit.jsonl")
    log = get_logger()
    app = FastAPI(title="OMC console", docs_url=None, redoc_url=None, openapi_url=None)
    templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
    token = secrets.token_urlsafe(24)

    def run_dir(name: str) -> Path:
        if not NAME_RE.match(name):
            raise HTTPException(404)
        d = (ws / "gates" / name).resolve()
        if ws / "gates" not in d.parents or not (d / "verdict.json").exists():
            raise HTTPException(404)
        return d

    def load_run(d: Path) -> dict:
        payload = json.loads((d / "verdict.json").read_text())
        word, sentence = headline(payload)
        head, _, rest = sentence.partition(". ")
        tol = float(payload["tolerance"]) * 1000
        val = float(payload["delta_lb"] if word == "REJECT" else payload["delta_ub"]) * 1000
        prog = int(round(100 * min(1.0, tol / max(float(payload["delta_ub"]) * 1000, tol))))
        return {"name": d.name, "payload": payload, "word": word, "chip": CHIP[word], "head": head + ".", "rest": rest,
                "tol": tol, "val": val, "progress": prog, "mtime": (d / "verdict.json").stat().st_mtime}

    def all_runs() -> list[dict]:
        base = ws / "gates"
        runs = [load_run(d) for d in sorted(base.iterdir()) if d.is_dir() and (d / "verdict.json").exists()] if base.exists() else []
        order = {"REJECT": 0, "HOLD": 1, "PROMOTE": 2}
        return sorted(runs, key=lambda r: (order[r["word"]], -r["mtime"]))

    def render(request: Request, name: str, ctx: dict):
        ctx = {"token": token, "per_1000": per_1000, "csp_nonce": request.state.csp_nonce, "user": request.state.user,
               "role": request.state.role, "auth_mode": auth_mode, **ctx}
        return templates.TemplateResponse(request, name, ctx)

    def labels_done(d: Path) -> dict[str, str]:
        p = d / "labels_collected.csv"
        return {r["case_id"]: r["gold"] for r in csv.DictReader(open(p, newline="", encoding="utf-8"))} if p.exists() else {}

    @app.middleware("http")
    async def guard(request: Request, call_next):
        start = time.perf_counter()
        request.state.request_id = uuid.uuid4().hex[:12]
        request.state.csp_nonce = new_nonce()
        request.state.user, request.state.role = "local", "admin"
        path = request.url.path
        denied = None
        if path not in ("/healthz", "/readyz") and auth_mode == "proxy":
            sent = request.headers.get("x-omc-proxy-secret", "")
            if not secrets.compare_digest(sent, proxy_secret):
                denied = (401, "authentication required")
                audit_log.append("unknown", "none", "auth_failed", path, "denied")
            else:
                user = request.headers.get("x-forwarded-user") or request.headers.get("x-auth-request-user") or ""
                groups = (request.headers.get("x-forwarded-groups") or request.headers.get("x-auth-request-groups") or "").split(",")
                role = resolve_role([g for g in groups if g.strip()], gmap)
                request.state.user, request.state.role = user or "unknown", role or "none"
                need = required_role(request.method, path)
                if not user or role is None or ROLE_RANK[role] < ROLE_RANK[need]:
                    denied = (403, "not permitted")
                    audit_log.append(request.state.user, request.state.role, "access_denied", f"{request.method} {path}", "denied")
        if denied:
            response = JSONResponse({"detail": denied[1]}, status_code=denied[0])
        else:
            response = await call_next(request)
        for k, v in security_headers(request.state.csp_nonce, hsts).items():
            response.headers[k] = v
        response.headers["X-Request-ID"] = request.state.request_id
        log.info("request", extra={"fields": {"request_id": request.state.request_id, "method": request.method, "path": path,
                                              "status": response.status_code, "ms": round((time.perf_counter() - start) * 1000, 1),
                                              "user": request.state.user}})
        return response

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz():
        ok = ws.is_dir() and os.access(ws, os.W_OK)      # the audit log needs a writable workspace
        return JSONResponse({"status": "ready" if ok else "not ready"}, status_code=200 if ok else 503)

    @app.get("/audit")
    def audit_page(request: Request):
        ok, msg = audit_log.verify()
        entries = audit_log.entries()[-200:][::-1]
        return render(request, "audit.html", {"entries": entries, "chain_ok": ok, "chain_msg": msg, "page": "audit"})

    @app.get("/audit/download")
    def audit_download(request: Request):
        audit_log.append(request.state.user, request.state.role, "audit_export", "admin-audit.jsonl")
        return FileResponse(audit_log.path, filename="admin-audit.jsonl")

    @app.get("/")
    def home(request: Request):
        exposure = json.loads((ws / "exposure.json").read_text()) if (ws / "exposure.json").exists() else []
        runs = all_runs()
        attention = [r for r in runs if r["word"] != "PROMOTE"]
        return render(request, "home.html", {"runs": runs, "exposure": exposure, "attention": attention, "page": "home"})

    @app.get("/verdict/{name}")
    def verdict(request: Request, name: str):
        d = run_dir(name)
        run = load_run(d)
        audit_log.append(request.state.user, request.state.role, "view_verdict", name)
        traj = json.loads((d / "trajectory.json").read_text()) if (d / "trajectory.json").exists() else {"points": []}
        count = int(round(run["val"]))
        label = f"1,000 cases with {count} marked as possibly worse"
        return render(request, "verdict.html", {
            "run": run, "dots": charts.dots_svg(count, int(round(run["tol"])), label),
            "chart": charts.trajectory_svg(traj["points"], run["tol"]), "page": "verdict",
            "fields": [(k, run["payload"][k]) for k in ("verdict", "tier", "tolerance", "alpha", "n_cases", "n_disagree", "n_labeled", "delta_ub", "delta_lb", "issued_at")]})

    @app.get("/evidence/{name}")
    def evidence(request: Request, name: str):
        d = run_dir(name)
        run = load_run(d)
        audit_log.append(request.state.user, request.state.role, "view_evidence", name)
        key = ws / "keys" / "omc-key.pub.pem"
        sig = {"state": "unknown", "text": "Public key not found in the workspace. Verify with the command below."}
        if key.exists():
            try:
                verify_statement((d / "verdict.cose").read_bytes(), load_public_key(key))
                sig = {"state": "ok", "text": "Signature valid: this statement is intact and was signed by the workspace key."}
            except ValueError as e:
                sig = {"state": "bad", "text": f"Signature check failed: {e}. Do not rely on this statement."}
        ok, msg = chain.verify_chain(d / "chain.jsonl") if (d / "chain.jsonl").exists() else (False, "no chain file")
        return render(request, "evidence.html", {"run": run, "sig": sig, "chain_ok": ok, "chain_msg": msg, "page": "evidence",
                                                  "files": sorted(f for f in FILES if (d / f).exists())})

    @app.get("/files/{name}/{fname}")
    def files(request: Request, name: str, fname: str):
        d = run_dir(name)
        if fname not in FILES or not (d / fname).exists():
            raise HTTPException(404)
        audit_log.append(request.state.user, request.state.role, "download_file", f"{name}/{fname}")
        return FileResponse(d / fname, filename=fname)

    @app.get("/setup")
    def setup(request: Request):
        ready = json.loads((ws / "readiness.json").read_text()) if (ws / "readiness.json").exists() else None
        return render(request, "setup.html", {"ready": ready, "page": "setup"})

    @app.get("/review/{name}")
    def review(request: Request, name: str):
        d = run_dir(name)
        qpath = d / "review_queue.csv"
        queue = list(csv.DictReader(open(qpath, newline="", encoding="utf-8"))) if qpath.exists() else []
        done = labels_done(d)
        pending = [q for q in queue if q["case_id"] not in done]
        known = sorted({q["option_1"] for q in queue} | {q["option_2"] for q in queue})
        return render(request, "review.html", {"run": load_run(d), "case": pending[0] if pending else None, "pending": len(pending),
                                               "done": len(done), "batch_pos": (len(done) % BATCH) + 1, "batch": BATCH, "known": known, "page": "review"})

    @app.post("/review/{name}/label")
    def label(request: Request, name: str, case_id: str = Form(...), choice: str = Form(...), custom: str = Form(""), tok: str = Form("")):
        if not secrets.compare_digest(tok, token):
            raise HTTPException(403, "bad form token")
        d = run_dir(name)
        queue = {r["case_id"]: r for r in csv.DictReader(open(d / "review_queue.csv", newline="", encoding="utf-8"))}
        if case_id not in queue:
            raise HTTPException(400, "unknown case")
        row = queue[case_id]
        gold = {"1": row["option_1"], "2": row["option_2"], "3": custom.strip()}.get(choice)
        if choice == "4":
            return RedirectResponse(f"/review/{name}", status_code=303)   # cannot tell: skipped for now
        if not gold:
            raise HTTPException(400, "a label is required")
        p = d / "labels_collected.csv"
        new = not p.exists()
        with open(p, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["case_id", "gold"])
            w.writerow([case_id, gold])
        audit_log.append(request.state.user, request.state.role, "label_submitted", f"{name}/{case_id}")
        return RedirectResponse(f"/review/{name}", status_code=303)

    return app

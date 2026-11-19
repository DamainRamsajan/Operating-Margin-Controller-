import json
import logging
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from omc.console.app import create_app  # noqa: E402
from omc.console.audit import AuditLog, verify_file  # noqa: E402
from omc.console.demo import build_workspace  # noqa: E402
from omc.console.security import check_bind_safety, resolve_role  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SECRET = "test-proxy-secret-value"


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return build_workspace(tmp_path_factory.mktemp("sws"), n=16000)


def proxy_client(ws):
    return TestClient(create_app(ws, auth_mode="proxy", proxy_secret=SECRET))


def hdr(user="amy@example.com", groups="omc-viewers", secret=SECRET):
    return {"X-OMC-Proxy-Secret": secret, "X-Forwarded-User": user, "X-Forwarded-Groups": groups}


def test_security_headers_and_unique_nonce(ws):
    c = TestClient(create_app(ws))
    r1, r2 = c.get("/"), c.get("/")
    csp = r1.headers["content-security-policy"]
    assert "script-src 'nonce-" in csp and "default-src 'none'" in csp and "frame-ancestors 'none'" in csp
    assert "unsafe-inline" not in re.search(r"script-src [^;]+", csp).group(0)
    n1 = re.search(r"script-src 'nonce-([^']+)'", csp).group(1)
    n2 = re.search(r"script-src 'nonce-([^']+)'", r2.headers["content-security-policy"]).group(1)
    assert n1 != n2 and f'nonce="{n1}"' in r1.text
    for h, v in (("x-frame-options", "DENY"), ("x-content-type-options", "nosniff"), ("referrer-policy", "no-referrer"), ("cache-control", "no-store")):
        assert r1.headers[h] == v
    assert r1.headers["x-request-id"]


def test_review_script_carries_the_nonce(ws):
    r = TestClient(create_app(ws)).get("/review/borderline-needs-labels")
    nonce = re.search(r"script-src 'nonce-([^']+)'", r.headers["content-security-policy"]).group(1)
    assert f'<script nonce="{nonce}">' in r.text


def test_health_endpoints_need_no_auth(ws, tmp_path):
    c = proxy_client(ws)
    assert c.get("/healthz").status_code == 200 and c.get("/readyz").status_code == 200
    missing = TestClient(create_app(tmp_path / "nope", auth_mode="proxy", proxy_secret=SECRET))
    assert missing.get("/readyz").status_code == 503


def test_proxy_mode_requires_the_shared_secret(ws):
    c = proxy_client(ws)
    assert c.get("/").status_code == 401
    assert c.get("/", headers=hdr(secret="wrong")).status_code == 401
    assert c.get("/", headers=hdr(groups="")).status_code == 403          # authenticated but no role
    assert c.get("/", headers=hdr(groups="some-other-group")).status_code == 403
    assert c.get("/", headers=hdr()).status_code == 200


def test_role_based_access(ws):
    c = proxy_client(ws)
    viewer, reviewer, admin = hdr(groups="omc-viewers"), hdr("rev@example.com", "omc-reviewers"), hdr("adm@example.com", "omc-admins")
    assert c.get("/verdict/clear-regression", headers=viewer).status_code == 200
    assert c.get("/audit", headers=viewer).status_code == 403 and c.get("/audit", headers=reviewer).status_code == 403
    assert c.get("/audit", headers=admin).status_code == 200
    page = c.get("/review/borderline-needs-labels", headers=viewer)
    token = re.search(r'name="tok" value="([^"]+)"', page.text).group(1)
    case = re.search(r'name="case_id" value="([^"]+)"', page.text).group(1)
    form = {"case_id": case, "choice": "1", "tok": token}
    assert c.post("/review/borderline-needs-labels/label", data=form, headers=viewer).status_code == 403
    assert c.post("/review/borderline-needs-labels/label", data=form, headers=reviewer, follow_redirects=False).status_code == 303


def test_multiple_groups_take_the_highest_role():
    m = {"a": "viewer", "b": "admin", "c": "reviewer"}
    assert resolve_role(["a", "c"], m) == "reviewer" and resolve_role(["a", "b", "c"], m) == "admin" and resolve_role(["x"], m) is None


def test_audit_log_records_and_detects_tampering(ws, tmp_path):
    c = proxy_client(ws)
    c.get("/evidence/benign-update", headers=hdr("aud@example.com", "omc-viewers"))
    c.get("/", headers=hdr(secret="bad"))
    path = ws / "audit" / "admin-audit.jsonl"
    entries = [json.loads(x) for x in path.read_text().splitlines()]
    actions = {e["action"] for e in entries}
    assert {"view_evidence", "auth_failed"} <= actions
    assert verify_file(path) == (True, "ok")
    copy = tmp_path / "log.jsonl"
    lines = path.read_text().splitlines()
    tampered = json.loads(lines[0])
    tampered["user"] = "someone-else"
    copy.write_text("\n".join([json.dumps(tampered, sort_keys=True), *lines[1:]]) + "\n")
    assert verify_file(copy)[0] is False
    cp = subprocess.run([sys.executable, "-m", "omc.cli", "audit-verify", str(copy)], capture_output=True, text=True, cwd=ROOT)
    assert cp.returncode == 1
    ok = subprocess.run([sys.executable, "-m", "omc.cli", "audit-verify", str(path)], capture_output=True, text=True, cwd=ROOT)
    assert ok.returncode == 0


def test_audit_log_append_is_chained(tmp_path):
    log = AuditLog(tmp_path / "a" / "log.jsonl")
    for i in range(3):
        log.append("u", "viewer", "view", f"t{i}")
    assert log.verify() == (True, "ok") and [e["seq"] for e in log.entries()] == [0, 1, 2]


def test_structured_logs_exclude_query_strings_and_secrets(ws):
    records = []

    class H(logging.Handler):
        def emit(self, record):
            records.append(record)

    lg = logging.getLogger("omc.console")
    h = H()
    lg.addHandler(h)
    try:
        TestClient(create_app(ws)).get("/?token=supersecret&x=1")
    finally:
        lg.removeHandler(h)
    fields = [r.fields for r in records if hasattr(r, "fields")]
    assert fields and fields[-1]["path"] == "/" and "supersecret" not in json.dumps(fields)
    assert fields[-1]["status"] == 200 and fields[-1]["request_id"]


def test_refuses_unauthenticated_non_local_bind():
    with pytest.raises(SystemExit):
        check_bind_safety("0.0.0.0", "none")
    check_bind_safety("127.0.0.1", "none")
    check_bind_safety("0.0.0.0", "proxy")
    check_bind_safety("0.0.0.0", "none", allow_insecure=True)


def test_proxy_mode_needs_a_secret(ws):
    with pytest.raises(ValueError):
        create_app(ws, auth_mode="proxy")

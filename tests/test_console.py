import csv
import re

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from omc.console.app import create_app  # noqa: E402
from omc.console.demo import build_workspace  # noqa: E402


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    return build_workspace(tmp_path_factory.mktemp("ws"), n=16000)


@pytest.fixture()
def client(ws):
    return TestClient(create_app(ws))


def test_home_lists_attention_and_exposure(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "What needs attention" in r.text and "REJECT" in r.text and "HOLD" in r.text
    assert "acme/llm-small@1.0" in r.text and "Critical" in r.text


def test_verdict_page_uses_plain_language_and_charts(client):
    r = client.get("/verdict/clear-regression")
    assert r.status_code == 200
    assert "per 1,000 cases" in r.text and r.text.count("<circle") == 1000 and "<polyline" in r.text
    assert "REJECT" in r.text and "Evidence grade" in r.text


def test_evidence_page_verifies_signature_and_chain(client):
    r = client.get("/evidence/benign-update")
    assert "Signature valid" in r.text and "Chain intact" in r.text


def test_tampered_statement_is_flagged(ws):
    d = ws / "gates" / "borderline"
    cose = bytearray((d / "verdict.cose").read_bytes())
    backup = bytes(cose)
    cose[-70] ^= 1
    (d / "verdict.cose").write_bytes(bytes(cose))
    try:
        r = TestClient(create_app(ws)).get("/evidence/borderline")
        assert "Signature invalid" in r.text
    finally:
        (d / "verdict.cose").write_bytes(backup)


def test_unknown_and_traversal_names_are_404(client):
    assert client.get("/verdict/nope").status_code == 404
    assert client.get("/verdict/..%2f..%2fetc").status_code == 404
    assert client.get("/files/benign-update/../../keys/omc-key.pub.pem").status_code in (404, 405)
    assert client.get("/files/benign-update/secret.txt").status_code == 404


def test_review_flow_requires_token_and_records_label(ws, client):
    page = client.get("/review/borderline-needs-labels")
    assert page.status_code == 200 and "Decision A" in page.text and "model names are hidden" in page.text
    assert "confidence" in page.text.lower()          # states that confidence is never shown
    case = re.search(r'name="case_id" value="([^"]+)"', page.text).group(1)
    bad = client.post("/review/borderline-needs-labels/label", data={"case_id": case, "choice": "1", "tok": "wrong"})
    assert bad.status_code == 403
    token = re.search(r'name="tok" value="([^"]+)"', page.text).group(1)
    ok = client.post("/review/borderline-needs-labels/label", data={"case_id": case, "choice": "1", "tok": token}, follow_redirects=False)
    assert ok.status_code == 303
    rows = list(csv.DictReader(open(ws / "gates" / "borderline-needs-labels" / "labels_collected.csv")))
    assert len(rows) == 1 and rows[0]["case_id"] == case
    nxt = re.search(r'name="case_id" value="([^"]+)"', client.get("/review/borderline-needs-labels").text).group(1)
    assert nxt != case


def test_review_requires_a_label_for_neither(client):
    page = client.get("/review/borderline-needs-labels")
    token = re.search(r'name="tok" value="([^"]+)"', page.text).group(1)
    case = re.search(r'name="case_id" value="([^"]+)"', page.text).group(1)
    r = client.post("/review/borderline-needs-labels/label", data={"case_id": case, "choice": "3", "custom": "", "tok": token})
    assert r.status_code == 400


def test_setup_page_shows_readiness(client):
    r = client.get("/setup")
    assert r.status_code == 200 and "Latest readiness check" in r.text and "Cases in both files" in r.text

from omc.privacy.gate import check_provider_terms, leakage_audit, leakage_upper_bound, redact


def test_redaction_patterns():
    text, c = redact("mail a.b@example.com card 4111 1111 1111 1111 ssn 123-45-6789 ip 10.0.0.1")
    assert "@" not in text and "4111" not in text and "123-45" not in text
    assert c["email"] == 1 and c["card"] == 1 and c["ssn"] == 1 and c["ipv4"] == 1


def test_non_luhn_digit_runs_are_not_redacted_as_cards():
    _text, c = redact("order 1234 5678 9012 3456 shipped")
    assert c["card"] == 0


def test_zero_leaks_upper_bound_matches_closed_form():
    ub = leakage_upper_bound(300, 0, 0.05)
    assert abs(ub - (1 - 0.05 ** (1 / 300))) < 1e-6


def test_leakage_audit_blocks_when_bound_exceeds_limit():
    assert leakage_audit(300, 0, 0.02)["decision"] == "release"
    assert leakage_audit(300, 6, 0.02)["decision"] == "block"
    assert leakage_audit(0, 0, 0.5)["decision"] == "block"


def test_provider_terms():
    pol = {"allow_training": False, "max_retention_days": 0, "allowed_regions": ["eu"]}
    assert check_provider_terms({"trains_on_data": False, "retention_days": 0, "region": "eu"}, pol) == []
    assert len(check_provider_terms({"trains_on_data": True, "retention_days": 30, "region": "us"}, pol)) == 3

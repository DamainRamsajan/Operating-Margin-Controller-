from omc.render import headline, per_1000

BASE = {"verdict": "promote", "tier": "tier0", "reason": "x", "tolerance": "0.010000", "alpha": "0.050000",
        "delta_ub": "0.009838", "delta_lb": "0.000000"}


def test_frequency_framing_is_per_1000():
    assert per_1000("0.0098") == "9.8"


def test_headline_texts():
    assert headline(BASE)[0] == "PROMOTE" and "at most 9.8 more wrong decisions per 1,000" in headline(BASE)[1]
    rej = {**BASE, "verdict": "reject", "delta_lb": "0.033"}
    assert headline(rej)[0] == "REJECT" and "at least 33.0" in headline(rej)[1]
    hold = {**BASE, "verdict": "hold", "reason": "more traffic needed"}
    assert headline(hold)[0] == "HOLD" and "More traffic needed." in headline(hold)[1]

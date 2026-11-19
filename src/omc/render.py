"""Plain-language rendering of verdicts (UX spec: verdict first, frequencies, grade on every number).
Used for CI pull-request comments, the console and reports."""
from __future__ import annotations


def per_1000(x) -> str:
    return f"{float(x) * 1000:.1f}"


def headline(p: dict) -> tuple[str, str]:
    """(status word, one-sentence meaning). All rates are shown per 1,000 cases."""
    tol = per_1000(p["tolerance"])
    conf = f"{(1 - float(p['alpha'])) * 100:.0f}%"
    v = p["verdict"]
    if v == "promote":
        return "PROMOTE", (f"No worse than the current model. With {conf} confidence the replacement makes at most "
                           f"{per_1000(p['delta_ub'])} more wrong decisions per 1,000 cases; your tolerance is {tol}.")
    if v == "reject":
        return "REJECT", (f"Worse than the current model. With {conf} confidence the replacement makes at least "
                          f"{per_1000(p['delta_lb'])} more wrong decisions per 1,000 cases; your tolerance is {tol}.")
    return "HOLD", (f"Not enough evidence yet. The replacement could make up to {per_1000(p['delta_ub'])} more wrong "
                    f"decisions per 1,000 cases; the evidence must show at most {tol}. {p['reason'].capitalize()}.")


def to_markdown(p: dict, key_hint: str = "<public key>") -> str:
    word, meaning = headline(p)
    s = p["subject"]
    stop = p["stopping_index"] if p["stopping_index"] is not None else "not reached"
    rows = [
        ("Change", f"{s['incumbent']} to {s['candidate']} ({s['workflow']})"),
        ("Cases scored", f"{p['n_cases']:,} ({p['n_disagree']:,} disagreed)"),
        ("Labels used", f"{p['n_labeled']:,}"),
        ("Evidence grade", p["grade"]),
        ("Method", f"certified paired audit, {p['tier']}, valid under continuous monitoring"),
        ("Stopped at case", f"{stop}"),
    ]
    out = [f"## OMC verdict: {word}", "", f"**{meaning}**", "", "| | |", "|---|---|"]
    out += [f"| {a} | {b} |" for a, b in rows]
    st = p.get("stationarity")
    if st and st.get("warning"):
        out += ["", f"**Warning:** the disagreement rate moved from {st['first_half_rate']} to {st['second_half_rate']} between the first and second half of the window. The guarantee assumes steady traffic; re-run on a stable window before relying on this result."]
    out += ["", "<details><summary>Technical detail</summary>", "",
            f"- alpha {p['alpha']}, tolerance {p['tolerance']} (error-rate difference)",
            f"- disagreement rate upper bound {p['rho_ub']}; regression bounds [{p['delta_lb']}, {p['delta_ub']}]",
            f"- label routing: {p['label_routing']['rule']}, rate {p['label_routing']['rate']} (never reads the outcome)",
            f"- assumptions: {'; '.join(p['assumptions'])}", "", "</details>", "",
            f"Verify offline: `omc-verify statement verdict.cose --pubkey {key_hint}`"]
    return "\n".join(out) + "\n"

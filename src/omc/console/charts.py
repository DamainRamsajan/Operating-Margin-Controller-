"""Server-side SVG charts for the console (no JavaScript needed to read a verdict)."""
from __future__ import annotations


def dots_svg(count: int, tolerance: int, label: str) -> str:
    out = [f'<svg role="img" aria-label="{label}" viewBox="0 0 500 104" width="100%" style="max-width:500px">']
    for i in range(1000):
        x, y = 5 + (i % 50) * 9.8, 5 + (i // 50) * 5
        hot = i < count
        extra = ' stroke="var(--ok)" stroke-width="0.8"' if (not hot and i < tolerance) else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="1.9" fill="{"var(--bad)" if hot else "var(--line)"}"{extra}/>')
    out.append("</svg>")
    return "".join(out)


def trajectory_svg(points: list[dict], tol: float) -> str:
    if not points:
        return "<p class='muted'>No trajectory recorded for this run.</p>"
    W, H, left, bottom, top, right = 640, 190, 38, 24, 8, 8
    xmax = points[-1]["n"]
    ymax = max(tol * 3, 20.0)
    def X(n): return left + (W - left - right) * n / xmax
    def Y(v): return H - bottom - (H - bottom - top) * min(v, ymax) / ymax
    def line(key, color):
        pts = " ".join(f"{X(p['n']):.1f},{Y(p[key]):.1f}" for p in points)
        return f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>'
    return (f'<svg role="img" aria-label="Upper and lower 95 percent bounds on extra wrong decisions per 1,000 cases versus cases scored" '
            f'viewBox="0 0 {W} {H}" width="100%">'
            f'<line x1="{left}" y1="{H - bottom}" x2="{W - right}" y2="{H - bottom}" stroke="var(--line)"/>'
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{H - bottom}" stroke="var(--line)"/>'
            f'<line x1="{left}" x2="{W - right}" y1="{Y(tol):.1f}" y2="{Y(tol):.1f}" stroke="var(--ok)" stroke-dasharray="5 4"/>'
            f'<text x="{W - right - 4}" y="{Y(tol) - 5:.1f}" text-anchor="end">tolerance {tol:.0f}</text>'
            + line("ub", "var(--accent)") + line("lb", "var(--bad)") +
            f'<text x="{left}" y="{H - 6}">0</text><text x="{W - right}" y="{H - 6}" text-anchor="end">{xmax:,} cases</text>'
            f'<text x="4" y="{top + 9}">{ymax:.0f} per 1,000</text></svg>')

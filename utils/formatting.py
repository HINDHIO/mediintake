"""
utils/formatting.py
HTML snippet helpers for urgency badges, symptom chips, etc.
"""


def urgency_html(urgency: str) -> str:
    """Return a coloured urgency badge as an HTML string."""
    lower = urgency.lower()
    if "high" in lower:
        return '<span class="urgency-badge urgency-high">🔴 High</span>'
    if "med" in lower:
        return '<span class="urgency-badge urgency-med">🟡 Medium</span>'
    if "low" in lower:
        return '<span class="urgency-badge urgency-low">🟢 Low</span>'
    return f'<span class="urgency-badge tag-gray">{urgency}</span>'


def symptom_tags(symptoms: list[str]) -> str:
    """Render a list of symptom strings as inline tag chips."""
    return "".join(
        f'<span class="tag tag-blue">{s.strip()}</span>'
        for s in symptoms
        if s.strip()
    )


def allergy_alert_html(flag_text: str) -> str:
    """Wrap an allergy/drug conflict message in a danger alert box."""
    return (
        '<div class="alert-box alert-danger">'
        '<div class="result-label" style="color:#dc2626;margin-bottom:.3rem">'
        "⚠ Allergy / Drug Conflict"
        "</div>"
        f'<div style="font-size:.88rem;color:#7f1d1d">{flag_text}</div>'
        "</div>"
    )


def action_item_html(priority: str, css_class: str, icon: str, action: str, rationale: str) -> str:
    """Render a single recommended-action row."""
    return (
        f'<div class="action-item">'
        f'<span class="action-icon">{icon}</span>'
        f'<span class="action-priority {css_class}">{priority}</span>'
        f"<span><b>{action}</b> "
        f'<span style="color:var(--muted);font-size:.82rem">— {rationale}</span></span>'
        f"</div>"
    )


def vital_chip_html(value: str, parameter: str, status: str, icon: str) -> str:
    """Render a single vitals display chip."""
    flag_cls = "abn" if status in ("Abnormal", "Critical") else "ok"
    return (
        '<div class="vital-chip">'
        f'<div class="vital-num">{value}</div>'
        f'<div class="vital-lbl">{parameter}</div>'
        f'<div class="vital-flag {flag_cls}">{icon} {status}</div>'
        "</div>"
    )
# utils/constants.py

# ── OpenAI ────────────────────────────────────────────────────────────────────
MODEL_NAME           = "gpt-4o-mini"
ANALYSIS_TEMPERATURE = 0.15
CHAT_TEMPERATURE     = 0.30
MAX_TOKENS           = 2048

# ── Urgency ───────────────────────────────────────────────────────────────────
URGENCY_COLORS = {
    "low":    "#16a34a",
    "medium": "#d97706",
    "high":   "#dc2626",
}

# ── Action priority ───────────────────────────────────────────────────────────
PRIORITY_CSS_CLASS = {
    "Stat":    "prio-stat",
    "Urgent":  "prio-urgent",
    "Routine": "prio-routine",
}

PRIORITY_ICONS = {
    "Stat":    "🚨",
    "Urgent":  "⚡",
    "Routine": "✅",
}

# ── Vital status ──────────────────────────────────────────────────────────────
STATUS_ICONS = {
    "Normal":   "🟢",
    "Abnormal": "🟡",
    "Critical": "🔴",
}

ABNORMAL_STATUSES = {"Abnormal", "Critical"}

# ── Likelihood tags (differential) ────────────────────────────────────────────
LIKELIHOOD_TAG_HTML = {
    "most likely": '<span class="tag tag-red"  style="font-size:.7rem">Most Likely</span>',
    "possible":    '<span class="tag tag-amber" style="font-size:.7rem">Possible</span>',
    "rule out":    '<span class="tag tag-gray"  style="font-size:.7rem">Rule Out</span>',
}

# ── Vitals input config ───────────────────────────────────────────────────────
# Tuple: (label, session_key, is_float, tooltip_text)
VITALS_CONFIG = [
    (
        "SBP", "sbp", False,
        "Systolic Blood Pressure (mmHg)\n"
        "Normal: 90–120 mmHg\nElevated: >130 mmHg\nHypertensive crisis: >180 mmHg",
    ),
    (
        "DBP", "dbp", False,
        "Diastolic Blood Pressure (mmHg)\n"
        "Normal: 60–80 mmHg\nElevated: >80 mmHg",
    ),
    (
        "HR", "hr", False,
        "Heart Rate (beats per minute)\n"
        "Normal: 60–100 bpm\nTachycardia: >100 bpm\nBradycardia: <60 bpm",
    ),
    (
        "Temp °C", "temp", True,
        "Body Temperature (°C)\n"
        "Normal: 36.1–37.2°C\nFever: >38°C\nHypothermia: <35°C",
    ),
    (
        "SpO₂ %", "spo2", False,
        "Oxygen Saturation (%)\n"
        "Normal: 95–100%\nMild hypoxia: 90–94%\nSevere: <90%",
    ),
    (
        "Wt kg", "weight", True,
        "Body Weight (kg)\nUsed for drug dosing calculations",
    ),
]

# ── PDF palette (hex strings for ReportLab) ───────────────────────────────────
PDF_COLORS = {
    "accent":  "#1d4ed8",
    "dark":    "#111827",
    "muted":   "#6b7280",
    "red":     "#dc2626",
    "amber":   "#d97706",
    "green":   "#16a34a",
    "border":  "#e4e7f0",
    "surface": "#f7f8fc",
    "soft":    "#eff3ff",
    "white":   "#ffffff",
}
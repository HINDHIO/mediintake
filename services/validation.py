"""
services/validation.py
Normalises and sanitises the raw dict returned by the AI before use in the UI
or PDF. Converts accidental wrong types, strips junk values, and guarantees
all expected keys exist with safe defaults.
"""

import re


def normalize_analysis(data: dict) -> dict:
    """
    Mutates *data* in-place and returns it after applying all normalisation
    rules. Safe to call on any dict, even a partially-formed one.
    """
    _normalize_symptoms(data)
    _normalize_allergy_flags(data)
    _set_defaults(data)
    return data


# ── Private helpers ───────────────────────────────────────────────────────────

def _normalize_symptoms(data: dict) -> None:
    """
    Ensure 'symptoms' is always a list of clean strings.
    The AI occasionally returns a comma/semicolon-separated string instead.
    """
    syms = data.get("symptoms", [])
    if isinstance(syms, str):
        syms = [s.strip() for s in re.split(r"[,;]", syms) if s.strip()]
    elif not isinstance(syms, list):
        syms = []
    data["symptoms"] = syms


def _normalize_allergy_flags(data: dict) -> None:
    """
    Ensure 'allergy_flags' is either a non-empty plain string or None.
    The AI occasionally returns a dict, list, or literal "null"/"none".
    """
    af = data.get("allergy_flags")

    # Discard any non-string structured type
    if isinstance(af, (dict, list)):
        af = None

    # Treat placeholder strings as null
    if isinstance(af, str) and af.strip().lower() in ("none", "n/a", "null", ""):
        af = None

    data["allergy_flags"] = af


def _set_defaults(data: dict) -> None:
    """
    Guarantee every expected top-level key exists so rendering code never
    needs to handle KeyError.
    """
    defaults = {
        "language":               "Unknown",
        "symptoms":               [],
        "urgency":                "Unknown",
        "department":             "General",
        "risk_reasoning":         "",
        "differential_diagnosis": [],
        "vitals_interpretation":  [],
        "recommended_actions":    [],
        "medications":            [],
        "allergy_flags":          None,
        "summary":                "",
    }
    for key, default in defaults.items():
        data.setdefault(key, default)
"""
services/prompt_builder.py
Constructs the system prompt and per-request user prompt sent to the LLM.
"""

from utils.vitals import vitals_summary
from schemas.analysis_schema import ANALYSIS_SCHEMA_STRING

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a senior clinical AI assistant supporting medical intake triage.\n"
    "You produce structured, clinically precise assessments.\n"
    "You ALWAYS respond with valid JSON only — no prose, no markdown fences, "
    "no explanation outside the JSON object.\n"
    "Every string value must be clean text; no embedded JSON or lists as strings."
)

# ── Prompt-building rules appended after the schema ──────────────────────────
SCHEMA_RULES = """
Rules:
- symptoms must be an array of strings, NOT a comma-separated string
- Each symptom is a short clean phrase (e.g. "chest pain radiating to left arm", "diaphoresis")
- differential_diagnosis must have 3-5 entries
- recommended_actions must have at least 4 entries
- If vitals are not provided, return vitals_interpretation as an empty array []
- allergy_flags must be a plain string or null — never a JSON object or array
- Return ONLY the JSON object, starting with { and ending with }
"""


def build_prompt(
    notes: str,
    history: str,
    allergies: str,
    meds_text: str,
    vitals: dict,
) -> str:
    """
    Compose the full user-turn prompt from structured intake fields.

    Args:
        notes:     Free-text patient notes (any language).
        history:   Past medical history.
        allergies: Known allergy list.
        meds_text: Current medications as free text.
        vitals:    Dict with keys: sbp, dbp, hr, temp, spo2, weight.

    Returns:
        A single prompt string ready to send as the user message.
    """
    vs = vitals_summary(vitals) if any(vitals.values()) else "Not provided"

    return f"""Analyze the following patient intake data and return a single JSON object.

=== PATIENT DATA ===
Patient Notes (may be in any language): {notes}
Medical History: {history or 'None provided'}
Known Allergies: {allergies or 'None provided'}
Current Medications: {meds_text or 'None provided'}
Vitals: {vs}

=== REQUIRED JSON SCHEMA ===
{ANALYSIS_SCHEMA_STRING}
{SCHEMA_RULES}"""
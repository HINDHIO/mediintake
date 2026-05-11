"""
ui/medication_tab.py
Renders the "Medication Analysis" tab with per-drug cards showing
class, indication, dosage, interactions, and warnings.
"""

import streamlit as st

from schemas.medication_schema import (
    MEDICATION_DISPLAY_FIELDS,
    MEDICATION_FIELD_FALLBACK,
    MEDICATION_WARNING_FIELD,
)


def render_medication_tab(d: dict) -> None:
    """Render the medication analysis card."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">💊 Medication Analysis</div>',
        unsafe_allow_html=True,
    )

    meds = d.get("medications", [])
    if not meds:
        st.markdown(
            '<p style="color:var(--muted);font-size:.88rem">'
            "No medications were identified in the patient data."
            "</p>",
            unsafe_allow_html=True,
        )
    else:
        for med in meds:
            _render_medication_card(med)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_medication_card(med: dict) -> None:
    name = med.get("name", "Unknown")

    # Build the detail rows from the schema-defined field order
    detail_lines = "".join(
        f"<b>{label}:</b> {med.get(key, MEDICATION_FIELD_FALLBACK)}<br>"
        for key, label in MEDICATION_DISPLAY_FIELDS
    )

    warning_key, _ = MEDICATION_WARNING_FIELD
    warning_text   = med.get(warning_key, MEDICATION_FIELD_FALLBACK)

    st.markdown(
        f"""
        <div class="med-card">
          <div class="med-name">💊 {name}</div>
          <div class="med-detail">{detail_lines}</div>
          <div class="med-warning">⚠ {warning_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
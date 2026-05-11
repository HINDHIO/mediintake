"""
ui/assessment_tab.py
Renders the "Assessment" tab: triage overview, symptoms, risk reasoning,
vitals interpretation, allergy flags, recommended actions, clinical summary,
and the PDF download button.
"""

from datetime import datetime

import streamlit as st

from pdf.report_generator import generate_pdf
from utils.constants import (
    ABNORMAL_STATUSES,
    PRIORITY_CSS_CLASS,
    PRIORITY_ICONS,
    STATUS_ICONS,
)
from utils.formatting import (
    action_item_html,
    allergy_alert_html,
    symptom_tags,
    urgency_html,
    vital_chip_html,
)


def render_assessment_tab(d: dict) -> None:
    """Render the full assessment card and PDF download."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Triage Overview</div>', unsafe_allow_html=True)

    _render_triage_grid(d)
    _render_symptoms(d)
    _render_risk_reasoning(d)
    _render_vitals_interpretation(d)
    _render_allergy_flags(d)
    _render_recommended_actions(d)
    _render_summary(d)

    st.markdown("</div>", unsafe_allow_html=True)

    _render_pdf_download(d)


# ── Private section renderers ─────────────────────────────────────────────────

def _render_triage_grid(d: dict) -> None:
    urgency = d.get("urgency", "")
    st.markdown(
        f"""
        <div class="result-grid">
          <div class="result-item">
            <div class="result-label">Detected Language</div>
            <div class="result-value">🌐 {d.get('language', '—')}</div>
          </div>
          <div class="result-item">
            <div class="result-label">Urgency Level</div>
            <div class="result-value">{urgency_html(urgency) if urgency else '—'}</div>
          </div>
          <div class="result-item span-2">
            <div class="result-label">Recommended Department</div>
            <div class="result-value">🏥 {d.get('department', '—')}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_symptoms(d: dict) -> None:
    syms = d.get("symptoms", [])
    if not syms:
        return
    tags_html = symptom_tags(syms)
    st.markdown(
        f'<div style="margin-bottom:.9rem">'
        f'<div class="result-label" style="margin-bottom:.45rem">Reported Symptoms</div>'
        f"{tags_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_risk_reasoning(d: dict) -> None:
    reasoning = d.get("risk_reasoning", "")
    if not reasoning:
        return
    st.markdown(
        f'<div class="result-label" style="margin-bottom:.4rem">Clinical Risk Reasoning</div>'
        f'<div class="reasoning-block">{reasoning}</div>',
        unsafe_allow_html=True,
    )


def _render_vitals_interpretation(d: dict) -> None:
    vi = d.get("vitals_interpretation", [])
    if not vi:
        return

    chips_html = "".join(
        vital_chip_html(
            value=v.get("value", "—"),
            parameter=v.get("parameter", ""),
            status=v.get("status", "Normal"),
            icon=STATUS_ICONS.get(v.get("status", "Normal"), "⚪"),
        )
        for v in vi
    )
    st.markdown(
        f'<div class="result-label" style="margin-bottom:.45rem">Vitals Interpretation</div>'
        f'<div class="vitals-row">{chips_html}</div>',
        unsafe_allow_html=True,
    )

    abnormal = [v for v in vi if v.get("status") in ABNORMAL_STATUSES]
    if abnormal:
        notes_html = "".join(
            f'<div style="font-size:.82rem;color:#7f1d1d;margin:.2rem 0">'
            f'⚠ <b>{v["parameter"]}:</b> {v["clinical_note"]}</div>'
            for v in abnormal
        )
        st.markdown(
            f'<div class="alert-box alert-danger" style="margin-top:.5rem">{notes_html}</div>',
            unsafe_allow_html=True,
        )


def _render_allergy_flags(d: dict) -> None:
    flag = d.get("allergy_flags")
    if flag:
        st.markdown(allergy_alert_html(flag), unsafe_allow_html=True)


def _render_recommended_actions(d: dict) -> None:
    actions = d.get("recommended_actions", [])
    if not actions:
        return

    items_html = "".join(
        action_item_html(
            priority=a.get("priority", "Routine"),
            css_class=PRIORITY_CSS_CLASS.get(a.get("priority", "Routine"), "prio-routine"),
            icon=PRIORITY_ICONS.get(a.get("priority", "Routine"), "✅"),
            action=a.get("action", ""),
            rationale=a.get("rationale", ""),
        )
        for a in actions
    )
    st.markdown(
        f'<div class="result-label" style="margin:.9rem 0 .45rem">Recommended Actions</div>'
        f"{items_html}",
        unsafe_allow_html=True,
    )


def _render_summary(d: dict) -> None:
    summary = d.get("summary", "")
    if not summary:
        return
    st.markdown(
        f'<div style="margin-top:.9rem">'
        f'<div class="result-label" style="margin-bottom:.4rem">Clinical Summary</div>'
        f'<div class="summary-text">{summary}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_pdf_download(d: dict) -> None:
    pdf_bytes = generate_pdf(d)
    filename  = f"MediIntake_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    st.download_button(
        label="⬇ Download Full PDF Report",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True,
    )
"""
ui/differential_tab.py
Renders the "Differential Diagnosis" tab with ranked, colour-coded
diagnosis cards including likelihood tags and clinical reasoning.
"""

import streamlit as st

from utils.constants import LIKELIHOOD_TAG_HTML


def render_differential_tab(d: dict) -> None:
    """Render the differential diagnosis card."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">🔬 Differential Diagnosis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="font-size:.83rem;color:var(--muted);margin-bottom:.85rem">'
        'Ranked by clinical likelihood given symptoms, history, and vitals. '
        '"Rule out" entries indicate diagnoses that must be actively excluded.'
        "</p>",
        unsafe_allow_html=True,
    )

    dd = d.get("differential_diagnosis", [])
    if not dd:
        st.markdown(
            '<p style="color:var(--muted);font-size:.88rem">No differential generated.</p>',
            unsafe_allow_html=True,
        )
    else:
        for item in dd:
            _render_diagnosis_item(item)

    st.markdown("</div>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_diagnosis_item(item: dict) -> None:
    likelihood = item.get("likelihood", "")
    lk         = likelihood.lower()

    rank_class = "diff-rank rule-out" if "rule" in lk else "diff-rank"
    tag_html   = LIKELIHOOD_TAG_HTML.get(
        lk,
        f'<span class="tag tag-gray" style="font-size:.7rem">{likelihood}</span>',
    )

    st.markdown(
        f"""
        <div class="diff-item">
          <div class="{rank_class}">{item.get('rank', '')}</div>
          <div>
            <div class="diff-name">{item.get('diagnosis', '—')} {tag_html}</div>
            <div class="diff-why">{item.get('reasoning', '')}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
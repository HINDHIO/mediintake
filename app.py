# app.py
# MediIntake · AI Medical Intake Agent
# Run with: streamlit run app.py

import json
import os
import sys

# Ensure project root is always on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from services.ai_analysis import run_analysis
from ui.assessment_tab import render_assessment_tab
from ui.chat_tab import render_chat_tab
from ui.differential_tab import render_differential_tab
from ui.medication_tab import render_medication_tab
from ui.styles import inject_styles
from utils.constants import VITALS_CONFIG

# ── Bootstrap ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MediIntake · AI Medical Intake",
    page_icon="🩺",
    layout="centered",
)

inject_styles()

# ── Password gate ─────────────────────────────────────────────────────────────
def _check_password() -> None:
    """
    Block the entire app behind a password.
    - Locally: password comes from .streamlit/secrets.toml
    - On Streamlit Cloud: password comes from the Secrets dashboard
    Falls back to 'mediintake2025' if no secret is set.
    """
    if st.session_state.get("authenticated"):
        return

    # Login UI
    st.markdown(
        """
        <div class="hero">
          <div class="hero-badge">🩺 AI-Powered · Multilingual · Clinical</div>
          <h1>Medical Intake Agent</h1>
          <p>Enter the demo password to access the application.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card" style="max-width:400px;margin:0 auto">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔒 Demo Access</div>', unsafe_allow_html=True)

    pwd = st.text_input(
        "Password",
        type="password",
        placeholder="Enter demo password",
        key="login_pwd",
    )

    if st.button("Enter →", key="login_btn"):
        correct = st.secrets.get("DEMO_PASSWORD", "mediintake2025")
        if pwd == correct:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

    st.markdown(
        '<p style="font-size:.78rem;color:var(--muted);margin-top:.75rem;text-align:center">'
        "Demo password available in the GitHub README."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()   # Nothing below renders until authenticated


_check_password()

# ── Session state defaults ────────────────────────────────────────────────────
for _key, _val in [("analysis", None), ("chat_history", []), ("chat_context", "")]:
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">🩺 AI-Powered · Multilingual · Clinical</div>
      <h1>Medical Intake Agent</h1>
      <p>Enter patient data in any language — receive a full differential diagnosis and clinical action plan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="card" style="margin-top:0">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📋 Patient Information</div>', unsafe_allow_html=True)

patient_notes = st.text_area(
    "Patient Notes *",
    placeholder=(
        'Describe symptoms in any language, e.g. "Severe chest pain radiating to left arm '
        'and jaw for 2 hours, diaphoresis, short of breath…"'
    ),
    height=130,
)

col_left, col_right = st.columns(2)
with col_left:
    medical_history = st.text_area(
        "Medical History",
        placeholder="e.g. Type 2 diabetes (2018), hypertension, appendectomy (2020)",
        height=88,
    )
with col_right:
    allergies = st.text_area(
        "Known Allergies",
        placeholder="e.g. Penicillin (rash), aspirin (GI intolerance), peanuts",
        height=88,
    )

current_meds = st.text_area(
    "Current Medications",
    placeholder="e.g. Metformin 500mg BD, Lisinopril 10mg OD, Atorvastatin 20mg nocte",
    height=75,
)

# ── Vitals inputs ─────────────────────────────────────────────────────────────
st.markdown(
    '<hr class="section-divider">'
    '<div class="card-title">💓 Vitals '
    '<span style="font-weight:400;text-transform:none;letter-spacing:0;font-size:.75rem">'
    "(optional — include any you have)"
    "</span></div>",
    unsafe_allow_html=True,
)

vitals: dict = {}
vital_cols = st.columns(len(VITALS_CONFIG))
for col, (label, key, is_float, tooltip) in zip(vital_cols, VITALS_CONFIG):
    with col:
        if is_float:
            raw = st.number_input(
                label, min_value=0.0, max_value=500.0, value=0.0, step=0.1, help=tooltip
            )
        else:
            raw = st.number_input(
                label, min_value=0, max_value=500, value=0, step=1, help=tooltip
            )
        vitals[key] = raw or None   # treat zero as "not provided"

st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
analyze_clicked = st.button("🔍 Run Clinical Analysis")
st.markdown("</div>", unsafe_allow_html=True)

# ── Run analysis ──────────────────────────────────────────────────────────────
if analyze_clicked:
    if not patient_notes.strip():
        st.warning("Please enter patient notes before analyzing.")
    else:
        with st.spinner("Running clinical analysis…"):
            try:
                result = run_analysis(
                    notes=patient_notes,
                    history=medical_history,
                    allergies=allergies,
                    meds_text=current_meds,
                    vitals=vitals,
                )
                st.session_state.analysis     = result
                st.session_state.chat_history = []
                st.session_state.chat_context = json.dumps(result, indent=2)
            except Exception as exc:
                st.error(f"Analysis error: {exc}")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.analysis:
    d = st.session_state.analysis

    tab_assessment, tab_differential, tab_medications, tab_chat = st.tabs(
        ["📊 Assessment", "🔬 Differential", "💊 Medications", "💬 Follow-up Chat"]
    )

    with tab_assessment:
        render_assessment_tab(d)

    with tab_differential:
        render_differential_tab(d)

    with tab_medications:
        render_medication_tab(d)

    with tab_chat:
        render_chat_tab(d)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="disclaimer">
      <span>⚠ Educational demo only.</span> &nbsp;This tool does not provide medical advice,
      diagnosis, or treatment. Always consult a qualified healthcare professional.
    </div>
    """,
    unsafe_allow_html=True,
)
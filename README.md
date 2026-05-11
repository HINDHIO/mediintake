# MediIntake · AI Medical Intake Agent

> **Educational demo only.** Not medical advice. Always consult a qualified clinician.

## Overview

MediIntake is a Streamlit application that accepts multilingual patient intake notes and returns a full clinical analysis powered by GPT-4o-mini, including:

- Urgency triage & recommended department
- Differential diagnosis (ranked, with reasoning)
- Vitals interpretation
- Recommended clinical actions (Stat / Urgent / Routine)
- Medication analysis with warnings & interactions
- Allergy / drug conflict detection
- Downloadable PDF report
- Follow-up chat grounded in the completed assessment

---

## Project Structure

```
mediintake/
│
├── app.py                     # Streamlit entry point
│
├── ui/
│   ├── styles.py              # Full CSS injection
│   ├── assessment_tab.py      # Tab 1 — triage overview + PDF download
│   ├── differential_tab.py    # Tab 2 — ranked differential diagnosis
│   ├── medication_tab.py      # Tab 3 — per-drug analysis cards
│   └── chat_tab.py            # Tab 4 — follow-up chat interface
│
├── services/
│   ├── ai_analysis.py         # LLM call → normalised result dict
│   ├── chat_service.py        # Follow-up chat completions
│   ├── prompt_builder.py      # System prompt + user prompt factory
│   └── validation.py          # Post-parse normalisation & defaults
│
├── pdf/
│   └── report_generator.py    # ReportLab A4 PDF builder
│
├── utils/
│   ├── vitals.py              # vitals_summary() helper
│   ├── formatting.py          # HTML snippet helpers (badges, chips, tags)
│   └── constants.py           # Shared constants (model, colours, config)
│
├── schemas/
│   ├── analysis_schema.py     # Full JSON schema + field docs + constraints
│   ├── medication_schema.py   # Medication field definitions
│   └── diagnosis_schema.py    # Differential diagnosis field definitions
│
├── assets/
│   └── logo.png               # (optional) brand logo
│
├── .env                       # OPENAI_API_KEY (never commit)
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Quick Start

```bash
# 1. Clone / copy project
cd mediintake

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# 5. Run
streamlit run app.py
```

---

## Configuration

| Variable        | Location            | Purpose                       |
|-----------------|---------------------|-------------------------------|
| `OPENAI_API_KEY`| `.env`              | OpenAI authentication         |
| `MODEL_NAME`    | `utils/constants.py`| LLM model (default gpt-4o-mini)|
| `ANALYSIS_TEMPERATURE` | `utils/constants.py` | Analysis creativity (0.15) |
| `CHAT_TEMPERATURE`     | `utils/constants.py` | Chat creativity (0.30)     |

---

## Disclaimer

This software is provided for **educational and demonstration purposes only**. It does not constitute medical advice, clinical diagnosis, or treatment recommendations. Always consult a qualified healthcare professional for any medical decisions.
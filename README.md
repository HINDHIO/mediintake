<div align="center">

# 🩺 MediIntake — AI Medical Intake Agent

**Multilingual · Differential Diagnosis · Clinical Action Plans · PDF Reports**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Engine-4A90D9?style=flat-square)](https://www.reportlab.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

### [🚀 Live Demo](https://mediintake-j2pmxsrtnud4cffqsqunzc.streamlit.app/) &nbsp;·&nbsp; Demo password: `mediintake2025`

> ⚠️ **Educational demo only.** Not a substitute for professional medical advice, diagnosis, or treatment.

</div>

---

## 🔍 What It Does

MediIntake is an AI-powered clinical intake assistant that transforms free-text patient notes
— in **any language** — into a structured, clinically precise triage report in seconds.

Enter patient notes, medical history, allergies, medications, and optional vitals.
The app returns:

| Output | Detail |
|---|---|
| **Urgency Triage** | Low / Medium / High with clinical reasoning |
| **Differential Diagnosis** | 3–5 ranked diagnoses with likelihood and reasoning |
| **Vitals Interpretation** | Flags abnormal values with clinical significance |
| **Recommended Actions** | Prioritised Stat / Urgent / Routine action plan |
| **Medication Analysis** | Drug class, dosage, warnings, and interaction flags |
| **Allergy Conflict Detection** | Automatic allergy–drug cross-checking |
| **PDF Report** | Downloadable A4 clinical handoff document |
| **Follow-up Chat** | Ask questions grounded in the completed assessment |

---

## 🧪 Try It — Sample Input

Use this in the live demo for a high-impact result:

| Field | Value |
|---|---|
| **Patient Notes** | *58-year-old male, sudden severe chest pain radiating to left arm and jaw, onset 2 hours ago. Associated diaphoresis and shortness of breath. Denies trauma.* |
| **Medical History** | *Type 2 diabetes (2014), hypertension, smoker 20 pack-years* |
| **Allergies** | *Penicillin (anaphylaxis), aspirin (GI intolerance)* |
| **Medications** | *Metformin 500mg BD, Lisinopril 10mg OD, Atorvastatin 20mg nocte* |
| **Vitals** | *SBP 168, DBP 98, HR 112, SpO2 94* |

---

## 🏗️ Architecture

Production-style modular Python — not a single script.
Strict one-way dependency flow: `schemas / utils` → `services` → `pdf` → `ui` → `app.py`

```
mediintake/
│
├── app.py                        # Entry point — layout, routing, password gate
│
├── ui/                           # Presentation layer — no business logic
│   ├── styles.py                 # Full CSS injection
│   ├── assessment_tab.py         # Triage overview + PDF download
│   ├── differential_tab.py       # Ranked differential diagnosis
│   ├── medication_tab.py         # Per-drug analysis cards
│   └── chat_tab.py               # Follow-up chat interface
│
├── services/                     # Business logic layer
│   ├── ai_analysis.py            # OpenAI API call → normalised result dict
│   ├── chat_service.py           # Follow-up chat completions
│   ├── prompt_builder.py         # System + user prompt factory
│   └── validation.py             # Post-parse normalisation & safe defaults
│
├── pdf/
│   └── report_generator.py       # ReportLab A4 PDF builder
│
├── utils/                        # Pure helpers — zero side effects
│   ├── constants.py              # Every magic string/number in one place
│   ├── vitals.py                 # Vitals summary formatter
│   └── formatting.py             # HTML snippet factories
│
└── schemas/                      # Data contracts — no project imports
    ├── analysis_schema.py        # JSON schema injected into LLM prompt
    ├── medication_schema.py      # Medication field definitions
    └── diagnosis_schema.py       # Differential diagnosis field definitions
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit · Custom CSS (DM Sans + DM Serif Display) |
| **AI / LLM** | OpenAI GPT-4o-mini · JSON mode enforced |
| **PDF Generation** | ReportLab — pure Python, no external binaries |
| **Auth** | Session-based password gate via Streamlit secrets |
| **Config** | python-dotenv (local) · Streamlit secrets (cloud) |
| **Language** | Python 3.10+ |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

```bash
# 1. Clone
git clone https://github.com/https://github.com/HINDHIO/mediintake.git
cd mediintake

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your local secrets file
# Windows:
mkdir .streamlit
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# macOS / Linux:
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 5. Open .streamlit/secrets.toml and add your real values:
#    OPENAI_API_KEY = "sk-your-real-key-here"
#    DEMO_PASSWORD  = "mediintake2025"

# 6. Run
streamlit run app.py
```

App opens at **http://localhost:8501** — password is whatever you set in `secrets.toml`.

---

## 🔐 Secrets & Environment

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | Your OpenAI API key |
| `DEMO_PASSWORD` | ✅ | Password shown on the login screen |

- **Local:** add both to `.streamlit/secrets.toml` — this file is in `.gitignore` and never committed
- **Streamlit Cloud:** paste both into the Secrets box in your app dashboard

---

## 🌍 Multilingual Support

Patient notes can be submitted in any language. The AI detects the language
automatically and returns the full structured analysis in English.
Tested with English, Arabic, French, Spanish, Italian, and German input.

---

## 🗺️ Roadmap

- [ ] ICD-10 code mapping on differential diagnoses
- [ ] SQLite persistence for longitudinal patient history
- [ ] FHIR-compliant export format
- [ ] Unit test suite for service and utility layers

---

## ⚠️ Disclaimer

Built for **educational and portfolio demonstration purposes only**.
Not medical advice. Never use AI-generated output as a substitute for a qualified clinician.

---

## 📝 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
Built by <a href="https://github.com/HINDHIO">Hind Faiz</a>
&nbsp;·&nbsp;
<a href="https://linkedin.com/in/hind-faiz-6b466a288">LinkedIn</a>
</div>

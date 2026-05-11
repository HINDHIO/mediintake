"""
schemas/analysis_schema.py
Defines the canonical JSON schema that the AI must return.
Imported by services/prompt_builder.py and used for validation.
"""

# Field-level documentation (used in validation messages and README)
FIELD_DOCS = {
    "language":               "Detected language of patient notes, expressed in English.",
    "symptoms":               "Array of short clean symptom phrases, one per element.",
    "urgency":                "Triage urgency: 'Low' | 'Medium' | 'High'.",
    "department":             "Recommended clinical department for the patient.",
    "risk_reasoning":         "2-4 sentences explaining the urgency decision with clinical references.",
    "differential_diagnosis": "3-5 ranked diagnoses; at least one 'Rule out' entry required.",
    "vitals_interpretation":  "One object per vital provided; empty array if no vitals given.",
    "recommended_actions":    "4-7 prioritised concrete clinical actions.",
    "medications":            "One object per medication found in the data; empty array if none.",
    "allergy_flags":          "Plain-text allergy/drug conflict description, or null if none.",
    "summary":                "2-3 sentence clinical handoff summary.",
}

# The schema injected verbatim into the LLM prompt
ANALYSIS_SCHEMA_STRING = """{
  "language": "detected language name in English",
  "symptoms": ["symptom 1", "symptom 2"],
  "urgency": "Low | Medium | High",
  "department": "recommended department",
  "risk_reasoning": "2-4 sentences explaining WHY this urgency level was assigned, referencing specific risk factors, symptom combinations, and red-flag features. Be clinically explicit.",
  "differential_diagnosis": [
    {
      "rank": 1,
      "diagnosis": "Diagnosis name",
      "likelihood": "Most likely | Possible | Rule out",
      "reasoning": "1-2 sentences on why this fits or must be excluded given the symptoms, history, and vitals"
    }
  ],
  "vitals_interpretation": [
    {
      "parameter": "e.g. Heart Rate",
      "value": "e.g. 112 bpm",
      "status": "Normal | Abnormal | Critical",
      "clinical_note": "1 sentence clinical significance"
    }
  ],
  "recommended_actions": [
    {
      "priority": "Stat | Urgent | Routine",
      "action": "specific clinical action",
      "rationale": "brief reason"
    }
  ],
  "medications": [
    {
      "name": "drug name",
      "class": "drug class",
      "usage": "indication",
      "dosage": "typical dosage range",
      "warnings": "key warnings relevant to this patient",
      "interactions": "interactions with other listed drugs or conditions"
    }
  ],
  "allergy_flags": "plain text description of any allergy-drug conflicts, or null if none",
  "summary": "2-3 sentence clinical summary suitable for handoff to a clinician"
}"""

# Minimum counts enforced during validation
SCHEMA_CONSTRAINTS = {
    "differential_diagnosis_min": 3,
    "differential_diagnosis_max": 5,
    "recommended_actions_min":    4,
}

# Required top-level keys — validation will warn if any are missing
REQUIRED_KEYS = [
    "language",
    "symptoms",
    "urgency",
    "department",
    "risk_reasoning",
    "differential_diagnosis",
    "recommended_actions",
    "medications",
    "allergy_flags",
    "summary",
]
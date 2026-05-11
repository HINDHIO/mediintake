"""
schemas/medication_schema.py
Field definitions and display labels for the medication schema.
Used by ui/medication_tab.py and pdf/report_generator.py.
"""

# Ordered list of (field_key, display_label) for rendering medication cards
MEDICATION_DISPLAY_FIELDS = [
    ("class",        "Drug Class"),
    ("usage",        "Indication"),
    ("dosage",       "Dosage"),
    ("interactions", "Interactions"),
]

# Field rendered separately with warning styling in the UI
MEDICATION_WARNING_FIELD = ("warnings", "Warnings")

# All expected keys in a medication object returned by the AI
MEDICATION_KEYS = [
    "name",
    "class",
    "usage",
    "dosage",
    "warnings",
    "interactions",
]

# Default fallback value when a field is missing or empty
MEDICATION_FIELD_FALLBACK = "—"
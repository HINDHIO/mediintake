"""
schemas/diagnosis_schema.py
Field definitions and display config for differential diagnosis items.
Used by ui/differential_tab.py and pdf/report_generator.py.
"""

# Valid likelihood values as returned by the AI
LIKELIHOOD_VALUES = ["Most likely", "Possible", "Rule out"]

# Mapping from lowercase likelihood key → CSS class applied to rank badge
RANK_BADGE_CLASS = {
    "rule out": "diff-rank rule-out",  # greyed badge
}
RANK_BADGE_DEFAULT_CLASS = "diff-rank"

# Ordered display fields for a differential item
DIAGNOSIS_DISPLAY_FIELDS = [
    ("rank",       "#"),
    ("diagnosis",  "Diagnosis"),
    ("likelihood", "Likelihood"),
    ("reasoning",  "Reasoning"),
]

# Column widths (mm) for the PDF table
PDF_COLUMN_WIDTHS_MM = [8, 44, 26, 92]
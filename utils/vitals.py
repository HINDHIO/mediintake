# utils/vitals.py

def vitals_summary(v: dict) -> str:
    parts = []
    if v.get("sbp") and v.get("dbp"):
        parts.append(f"BP {v['sbp']}/{v['dbp']} mmHg")
    if v.get("hr"):
        parts.append(f"HR {v['hr']} bpm")
    if v.get("temp"):
        parts.append(f"Temp {v['temp']}°C")
    if v.get("spo2"):
        parts.append(f"SpO2 {v['spo2']}%")
    if v.get("weight"):
        parts.append(f"Weight {v['weight']} kg")
    return " · ".join(parts) if parts else "Not provided"


def any_vitals_provided(v: dict) -> bool:
    return any(v.values())
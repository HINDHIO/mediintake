# pdf/report_generator.py

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph,
)

from utils.constants import PDF_COLORS
from utils.vitals import vitals_summary


def _c(key: str):
    return colors.HexColor(PDF_COLORS[key])


def _make_styles():
    dark  = _c("dark");  muted = _c("muted")
    acc   = _c("accent"); red  = _c("red")
    green = _c("green"); amber = _c("amber")
    return {
        "H1":        ParagraphStyle("H1",   fontName="Helvetica-Bold",    fontSize=20, textColor=dark,  spaceAfter=3),
        "Sub":       ParagraphStyle("Sub",  fontName="Helvetica-Oblique", fontSize=8,  textColor=muted, spaceAfter=0),
        "H2":        ParagraphStyle("H2",   fontName="Helvetica-Bold",    fontSize=11, textColor=acc,   spaceAfter=5, spaceBefore=14),
        "Body":      ParagraphStyle("Bd",   fontName="Helvetica",         fontSize=9,  textColor=dark,  spaceAfter=4, leading=14),
        "Small":     ParagraphStyle("Sm",   fontName="Helvetica-Oblique", fontSize=8,  textColor=muted, spaceAfter=2),
        "Bold":      ParagraphStyle("Bd2",  fontName="Helvetica-Bold",    fontSize=9,  textColor=dark,  spaceAfter=2),
        "LabelStyle":ParagraphStyle("Lbl",  fontName="Helvetica-Bold",    fontSize=8.5,textColor=muted, leading=12),
        "CellStyle": ParagraphStyle("Cel",  fontName="Helvetica",         fontSize=8.5,textColor=dark,  leading=13),
        "CellBold":  ParagraphStyle("CeB",  fontName="Helvetica-Bold",    fontSize=8.5,textColor=dark,  leading=13),
        "CellMuted": ParagraphStyle("CeM",  fontName="Helvetica",         fontSize=8,  textColor=muted, leading=12),
        "CellRed":   ParagraphStyle("CeR",  fontName="Helvetica-Bold",    fontSize=8,  textColor=red,   leading=12),
        "CellGreen": ParagraphStyle("CeG",  fontName="Helvetica-Bold",    fontSize=8,  textColor=green, leading=12),
        "CellAmber": ParagraphStyle("CeA",  fontName="Helvetica-Bold",    fontSize=8,  textColor=amber, leading=12),
        "HdrStyle":  ParagraphStyle("Hdr",  fontName="Helvetica-Bold",    fontSize=8.5,textColor=acc,   leading=12),
    }


def _base_table_style():
    border = _c("border")
    return [
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor(PDF_COLORS["soft"])),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("BOX",           (0, 0), (-1, -1), 0.5, border),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, border),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, colors.HexColor(PDF_COLORS["surface"])]),
    ]


def generate_pdf(d: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
          leftMargin=20*mm, rightMargin=20*mm, topMargin=22*mm, bottomMargin=20*mm)

    S = _make_styles()

    def P(text, style_key="CellStyle"):
        return Paragraph(str(text) if text else "—", S[style_key])

    def urgency_para_style(u):
        color_map = {"low": _c("green"), "medium": _c("amber"), "high": _c("red")}
        color = color_map.get(u.lower(), _c("dark"))
        return ParagraphStyle("Urg", fontName="Helvetica-Bold", fontSize=9,
                               textColor=color, alignment=1, leading=12)

    def status_sk(s):
        return {"Abnormal": "CellRed", "Critical": "CellRed", "Normal": "CellGreen"}.get(s, "CellAmber")

    def lh_sk(lh):
        lk = lh.lower()
        if "rule" in lk: return "CellAmber"
        if "most" in lk: return "CellRed"
        return "CellStyle"

    story = []

    # Header
    story.append(P("MediIntake · AI Medical Intake Report", "H1"))
    story.append(Spacer(1, 4*mm))
    story.append(P(f"Generated: {d['timestamp']}  |  Confidential – Educational Demo", "Sub"))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_c("accent"), spaceAfter=8))

    # Triage
    urg = d.get("urgency", "")
    triage = [
        [P("Language","HdrStyle"), P("Urgency","HdrStyle"), P("Department","HdrStyle")],
        [P(d.get("language","—"),"CellBold"),
         Paragraph(urg, urgency_para_style(urg)),
         P(d.get("department","—"),"CellBold")],
    ]
    t = Table(triage, colWidths=[50*mm, 50*mm, 70*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), _c("soft")),
        ("ALIGN",         (0,0),(-1,-1),"CENTER"),
        ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
        ("BOX",           (0,0),(-1,-1), 0.5, _c("border")),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, _c("border")),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ]))
    story.append(t); story.append(Spacer(1,6))

    # Patient context
    story.append(P("Patient Context","H2"))
    ctx = [
        [P("Patient Notes",  "LabelStyle"), P(d.get("notes","—"))],
        [P("Medical History","LabelStyle"), P(d.get("history","—") or "None provided")],
        [P("Allergies",      "LabelStyle"), P(d.get("allergies","—") or "None provided")],
        [P("Medications",    "LabelStyle"), P(d.get("meds_text","—") or "None provided")],
        [P("Vitals",         "LabelStyle"), P(vitals_summary(d.get("vitals",{})))],
    ]
    ct = Table(ctx, colWidths=[40*mm, 130*mm])
    ct.setStyle(TableStyle([
        ("VALIGN",         (0,0),(-1,-1),"TOP"),
        ("ROWBACKGROUNDS", (0,0),(-1,-1),[colors.HexColor(PDF_COLORS["surface"]), colors.white]),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 7),
        ("TOPPADDING",     (0,0),(-1,-1), 7),
        ("LEFTPADDING",    (0,0),(-1,-1), 7),
        ("BOX",            (0,0),(-1,-1), 0.5, _c("border")),
        ("INNERGRID",      (0,0),(-1,-1), 0.5, _c("border")),
    ]))
    story.append(ct)

    # Symptoms
    story.append(P("Reported Symptoms","H2"))
    syms = d.get("symptoms",[])
    story.append(P(", ".join(syms) if syms else "None identified","Body"))

    # Vitals interpretation
    vi = d.get("vitals_interpretation",[])
    if vi:
        story.append(P("Vitals Interpretation","H2"))
        rows = [[P("Parameter","HdrStyle"),P("Value","HdrStyle"),P("Status","HdrStyle"),P("Clinical Note","HdrStyle")]]
        for v in vi:
            s = v.get("status","Normal")
            rows.append([P(v.get("parameter",""),"CellBold"), P(v.get("value",""),"CellStyle"),
                         P(s, status_sk(s)), P(v.get("clinical_note",""),"CellStyle")])
        vt = Table(rows, colWidths=[35*mm,25*mm,22*mm,88*mm])
        vt.setStyle(TableStyle(_base_table_style()))
        story.append(vt); story.append(Spacer(1,4))

    # Risk reasoning
    if d.get("risk_reasoning"):
        story.append(P("Clinical Risk Reasoning","H2"))
        story.append(P(d["risk_reasoning"],"Body"))

    # Allergy flags
    if d.get("allergy_flags"):
        story.append(P("Allergy / Drug Conflict Flags","H2"))
        story.append(P(d["allergy_flags"],"CellRed"))

    # Differential
    dd = d.get("differential_diagnosis",[])
    if dd:
        story.append(P("Differential Diagnosis","H2"))
        rows = [[P("#","HdrStyle"),P("Diagnosis","HdrStyle"),P("Likelihood","HdrStyle"),P("Reasoning","HdrStyle")]]
        for item in dd:
            lh = item.get("likelihood","")
            rows.append([P(str(item.get("rank","")),"CellBold"), P(item.get("diagnosis",""),"CellBold"),
                         P(lh, lh_sk(lh)), P(item.get("reasoning",""),"CellStyle")])
        ddt = Table(rows, colWidths=[8*mm,44*mm,26*mm,92*mm])
        ddt.setStyle(TableStyle(_base_table_style()))
        story.append(ddt); story.append(Spacer(1,4))

    # Actions
    actions = d.get("recommended_actions",[])
    if actions:
        story.append(P("Recommended Actions","H2"))
        prio_sk = {"Stat":"CellRed","Urgent":"CellAmber","Routine":"CellGreen"}
        rows = [[P("Priority","HdrStyle"),P("Action","HdrStyle"),P("Rationale","HdrStyle")]]
        for a in actions:
            p = a.get("priority","Routine")
            rows.append([P(p, prio_sk.get(p,"CellStyle")), P(a.get("action",""),"CellBold"),
                         P(a.get("rationale",""),"CellMuted")])
        at = Table(rows, colWidths=[20*mm,75*mm,75*mm])
        at.setStyle(TableStyle(_base_table_style()))
        story.append(at); story.append(Spacer(1,4))

    # Medications
    meds = d.get("medications",[])
    if meds:
        story.append(P("Medication Analysis","H2"))
        for med in meds:
            story.append(P(f"<b>{med.get('name','Unknown')}</b>","Bold"))
            mr = [
                [P("Drug Class",  "LabelStyle"), P(med.get("class","—"))],
                [P("Indication",  "LabelStyle"), P(med.get("usage","—"))],
                [P("Dosage",      "LabelStyle"), P(med.get("dosage","—"))],
                [P("Warnings",    "LabelStyle"), P(med.get("warnings","—"),"CellRed")],
                [P("Interactions","LabelStyle"), P(med.get("interactions","—"))],
            ]
            mt = Table(mr, colWidths=[32*mm,138*mm])
            mt.setStyle(TableStyle([
                ("VALIGN",         (0,0),(-1,-1),"TOP"),
                ("ROWBACKGROUNDS", (0,0),(-1,-1),[colors.HexColor(PDF_COLORS["surface"]), colors.white]),
                ("BOTTOMPADDING",  (0,0),(-1,-1), 6),
                ("TOPPADDING",     (0,0),(-1,-1), 6),
                ("LEFTPADDING",    (0,0),(-1,-1), 7),
                ("BOX",            (0,0),(-1,-1), 0.5, _c("border")),
                ("INNERGRID",      (0,0),(-1,-1), 0.5, _c("border")),
            ]))
            story.append(mt); story.append(Spacer(1,5))

    # Summary
    story.append(P("Clinical Summary","H2"))
    story.append(P(d.get("summary","—"),"Body"))

    # Footer
    story.append(Spacer(1,6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_c("border"), spaceAfter=4))
    story.append(P(
        "DISCLAIMER: This report is generated by an AI system for educational purposes only. "
        "It does not constitute medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare professional.", "Small"))

    doc.build(story)
    buf.seek(0)
    return buf.read()
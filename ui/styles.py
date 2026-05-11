"""
ui/styles.py
Injects the full application CSS into the Streamlit page.
Call inject_styles() once at the top of app.py, before rendering any widgets.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{
  --bg:#f7f8fc; --surface:#fff; --border:#e4e7f0; --text:#111827; --muted:#6b7280;
  --accent:#1d4ed8; --accent-soft:#eff3ff;
  --low:#16a34a; --low-bg:#f0fdf4;
  --med:#d97706; --med-bg:#fffbeb;
  --high:#dc2626; --high-bg:#fef2f2;
  --radius:12px; --shadow:0 1px 4px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.06);
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:var(--bg)!important;color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:2rem!important;max-width:820px!important;}

/* hero */
.hero{text-align:center;padding:2rem 1rem .75rem;}
.hero-badge{display:inline-block;font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft);border:1px solid #c7d7ff;border-radius:99px;padding:.25rem .85rem;margin-bottom:.9rem;}
.hero h1{font-family:'DM Serif Display',serif;font-size:2.1rem;font-weight:400;line-height:1.2;margin:0 0 .5rem;}
.hero p{font-size:.95rem;color:var(--muted);margin:0;}

/* card */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:1.5rem 1.75rem;margin-bottom:1.1rem;}
.card-title{font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.9rem;}
.section-divider{border:none;border-top:1px solid var(--border);margin:1.1rem 0;}

/* inputs */
.stTextArea textarea,.stTextInput input{border:1.5px solid var(--border)!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:.9rem!important;padding:.75rem 1rem!important;background:#fafbff!important;transition:border-color .2s;}
.stTextArea textarea:focus,.stTextInput input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(29,78,216,.10)!important;}
.stNumberInput input{border:1.5px solid var(--border)!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:.88rem!important;background:#fafbff!important;}

/* button */
.stButton > button{background:var(--accent)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:.9rem!important;padding:.6rem 1.6rem!important;width:100%!important;box-shadow:0 2px 8px rgba(29,78,216,.3)!important;transition:background .2s,transform .1s!important;}
.stButton > button:hover{background:#1e40af!important;transform:translateY(-1px)!important;}

/* result grid */
.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:.85rem;margin-bottom:1rem;}
.result-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.9rem 1.1rem;}
.result-label{font-size:.68rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin-bottom:.3rem;}
.result-value{font-size:.97rem;font-weight:500;}
.span-2{grid-column:span 2;}

/* urgency badges */
.urgency-badge{display:inline-block;font-size:.76rem;font-weight:700;border-radius:99px;padding:.2rem .8rem;}
.urgency-low{color:var(--low);background:var(--low-bg);border:1px solid #bbf7d0;}
.urgency-med{color:var(--med);background:var(--med-bg);border:1px solid #fde68a;}
.urgency-high{color:var(--high);background:var(--high-bg);border:1px solid #fecaca;}

/* tags */
.tag{display:inline-block;font-size:.76rem;font-weight:500;border-radius:99px;padding:.15rem .65rem;margin:.15rem .15rem .15rem 0;}
.tag-blue{background:var(--accent-soft);color:var(--accent);border:1px solid #c7d7ff;}
.tag-gray{background:#f3f4f6;color:#374151;border:1px solid #d1d5db;}
.tag-red{background:#fef2f2;color:#dc2626;border:1px solid #fecaca;}
.tag-amber{background:#fffbeb;color:#d97706;border:1px solid #fde68a;}

/* summary / reasoning */
.summary-text{font-size:.9rem;color:var(--text);line-height:1.7;background:var(--bg);border-left:3px solid var(--accent);border-radius:0 6px 6px 0;padding:.85rem 1.1rem;}
.reasoning-block{font-size:.88rem;color:var(--text);line-height:1.7;background:#fafbff;border:1px solid var(--border);border-radius:8px;padding:.9rem 1.1rem;margin-bottom:.7rem;}
.reasoning-block b{color:var(--accent);}

/* differential */
.diff-item{display:flex;align-items:flex-start;gap:.65rem;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;margin-bottom:.5rem;}
.diff-rank{font-size:.72rem;font-weight:700;color:#fff;background:var(--accent);border-radius:99px;min-width:1.4rem;height:1.4rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:.05rem;}
.diff-rank.rule-out{background:#9ca3af;}
.diff-name{font-size:.9rem;font-weight:600;color:var(--text);margin-bottom:.15rem;}
.diff-why{font-size:.8rem;color:var(--muted);line-height:1.5;}

/* actions */
.action-item{display:flex;align-items:center;gap:.65rem;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.6rem 1rem;margin-bottom:.4rem;font-size:.88rem;}
.action-icon{font-size:1rem;flex-shrink:0;}
.action-priority{font-size:.65rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;border-radius:99px;padding:.1rem .55rem;flex-shrink:0;}
.prio-stat{color:#dc2626;background:#fef2f2;border:1px solid #fecaca;}
.prio-urgent{color:#d97706;background:#fffbeb;border:1px solid #fde68a;}
.prio-routine{color:#16a34a;background:#f0fdf4;border:1px solid #bbf7d0;}

/* vitals chips */
.vitals-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.3rem;}
.vital-chip{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:.5rem .85rem;text-align:center;}
.vital-num{font-size:1rem;font-weight:600;color:var(--accent);}
.vital-lbl{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;}
.vital-flag{font-size:.65rem;font-weight:600;margin-top:.1rem;}
.vital-flag.abn{color:var(--high);}
.vital-flag.ok{color:var(--low);}

/* medications */
.med-card{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.9rem 1.1rem;margin-bottom:.65rem;}
.med-name{font-size:.97rem;font-weight:600;margin-bottom:.25rem;}
.med-detail{font-size:.82rem;color:var(--muted);line-height:1.6;}
.med-warning{font-size:.78rem;color:var(--high);margin-top:.35rem;font-weight:500;}

/* alert boxes */
.alert-box{border-radius:8px;padding:.85rem 1.1rem;margin-bottom:.9rem;}
.alert-danger{background:#fef2f2;border:1px solid #fecaca;}
.alert-warn{background:#fffbeb;border:1px solid #fde68a;}

/* chat */
.chat-bubble-user{background:var(--accent);color:#fff;border-radius:12px 12px 2px 12px;padding:.7rem 1rem;margin:.35rem 0;font-size:.88rem;max-width:80%;margin-left:auto;}
.chat-bubble-ai{background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:12px 12px 12px 2px;padding:.7rem 1rem;margin:.35rem 0;font-size:.88rem;max-width:90%;box-shadow:var(--shadow);}
.chat-label{font-size:.65rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:.12rem;}
.chat-wrap{max-height:360px;overflow-y:auto;padding:.4rem 0;}

/* disclaimer */
.disclaimer{text-align:center;font-size:.72rem;color:var(--muted);padding:1rem 0 2rem;border-top:1px solid var(--border);margin-top:.5rem;}
.disclaimer span{color:var(--high);font-weight:600;}

/* tabs */
.stTabs [data-baseweb="tab-list"]{gap:.5rem;border-bottom:2px solid var(--border);}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif;font-weight:500;font-size:.88rem;color:var(--muted);border-radius:6px 6px 0 0;padding:.5rem 1rem;}
.stTabs [aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
</style>
"""


def inject_styles() -> None:
    """Inject the full application CSS into the Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
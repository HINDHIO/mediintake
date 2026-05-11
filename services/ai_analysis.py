# services/ai_analysis.py
# Calls the OpenAI API and returns a normalised result dict.
# Reads the API key from Streamlit secrets (cloud) or .env (local).

import json
import os
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

from services.prompt_builder import SYSTEM_PROMPT, build_prompt
from services.validation import normalize_analysis
from utils.constants import MODEL_NAME, ANALYSIS_TEMPERATURE, MAX_TOKENS

load_dotenv()


def _get_client() -> OpenAI:
    """
    Return an authenticated OpenAI client.
    Priority order:
      1. st.secrets  — used when running on Streamlit Cloud
      2. os.environ  — used when running locally via .env / .streamlit/secrets.toml
    """
    try:
        import streamlit as st
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def run_analysis(notes: str, history: str, allergies: str,
                 meds_text: str, vitals: dict) -> dict:
    """
    Send intake data to the LLM and return a normalised analysis dict.

    Returned dict contains all AI fields plus metadata keys:
        raw, timestamp, notes, history, allergies, meds_text, vitals
    """
    client      = _get_client()
    user_prompt = build_prompt(notes, history, allergies, meds_text, vitals)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=ANALYSIS_TEMPERATURE,
        max_tokens=MAX_TOKENS,
        response_format={"type": "json_object"},
    )

    raw  = response.choices[0].message.content
    data = json.loads(raw)

    normalize_analysis(data)

    data.update({
        "raw":       raw,
        "timestamp": datetime.now().strftime("%d %B %Y, %H:%M"),
        "notes":     notes,
        "history":   history,
        "allergies": allergies,
        "meds_text": meds_text,
        "vitals":    vitals,
    })

    return data
# services/chat_service.py
# Follow-up chat completions grounded in the completed assessment.
# Reads the API key from Streamlit secrets (cloud) or .env (local).

import os

from openai import OpenAI
from dotenv import load_dotenv

from utils.constants import MODEL_NAME, CHAT_TEMPERATURE

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


_SYSTEM_TEMPLATE = (
    "You are MediIntake, a clinical AI intake assistant.\n"
    "A full assessment has been completed. Answer follow-up questions concisely and precisely.\n"
    "Reference specific findings from the assessment when relevant.\n"
    "Always recommend consulting a qualified clinician for personal medical decisions.\n\n"
    "=== ASSESSMENT CONTEXT ===\n"
    "{context}"
)


def chat_reply(user_message: str, assessment_context: str,
               history: list) -> str:
    """
    Generate a follow-up reply grounded in the completed assessment.

    Args:
        user_message:       The user's latest question.
        assessment_context: JSON string of the full analysis result dict.
        history:            List of {'role': ..., 'content': ...} dicts.

    Returns:
        The model's reply as a plain string.
    """
    client     = _get_client()
    system_msg = _SYSTEM_TEMPLATE.format(context=assessment_context)

    messages = (
        [{"role": "system", "content": system_msg}]
        + history
        + [{"role": "user", "content": user_message}]
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=CHAT_TEMPERATURE,
    )
    return response.choices[0].message.content
"""
ui/chat_tab.py
Renders the "Follow-up Chat" tab, including the conversation history,
the text input, send/clear buttons, and chat reply logic.
"""

import streamlit as st

from services.chat_service import chat_reply


def render_chat_tab(d: dict) -> None:
    """
    Render the follow-up chat interface.

    Reads and writes:
        st.session_state.chat_history  – list of {role, content} dicts
        st.session_state.chat_context  – JSON string of the full analysis
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">💬 Follow-up Questions</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="font-size:.83rem;color:var(--muted);margin-bottom:.75rem">'
        "Ask anything about this assessment — differential reasoning, drug interactions, "
        "urgency escalation, next steps, etc."
        "</p>",
        unsafe_allow_html=True,
    )

    _render_chat_history()
    _render_chat_input()

    st.markdown("</div>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_chat_history() -> None:
    history = st.session_state.get("chat_history", [])
    if not history:
        return

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in history:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="text-align:right">'
                f'<div class="chat-label" style="text-align:right">You</div>'
                f'<div class="chat-bubble-user">{msg["content"]}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div>'
                f'<div class="chat-label">MediIntake AI</div>'
                f'<div class="chat-bubble-ai">{msg["content"]}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_chat_input() -> None:
    chat_input = st.text_input(
        "Question",
        placeholder=(
            "e.g. Why is aortic dissection listed as rule-out? "
            "What's the troponin test for?"
        ),
        label_visibility="collapsed",
        key="chat_inp",
    )

    send_col, clear_col = st.columns([4, 1])
    with send_col:
        send_clicked = st.button("Send →", key="send_btn")
    with clear_col:
        if st.button("Clear", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

    if send_clicked and chat_input.strip():
        with st.spinner("Thinking…"):
            try:
                reply = chat_reply(
                    user_message=chat_input,
                    assessment_context=st.session_state.chat_context,
                    history=st.session_state.chat_history,
                )
                st.session_state.chat_history.append(
                    {"role": "user", "content": chat_input}
                )
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )
                st.rerun()
            except Exception as exc:
                st.error(f"Chat error: {exc}")
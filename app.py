import uuid
import streamlit as st

from graph.farmer_graph import farmer_graph

from service.sqlite_service import (
    init_db,
    save_message,
    get_threads,
    get_thread_messages,
    delete_thread
)

from service.vector_service import create_vectorstore


st.set_page_config(
    page_title="Farmer AI",
    layout="wide"
)

init_db()
create_vectorstore()


# =========================
# SESSION STATE
# =========================

if "thread_name" not in st.session_state:
    st.session_state.thread_name = f"Chat-{uuid.uuid4().hex[:6]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "delete_confirm_thread" not in st.session_state:
    st.session_state.delete_confirm_thread = None


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🌾 Farmer AI Assistant")
    st.caption("With Dr. Krunal Kamani")

    # NEW CHAT
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.thread_name = f"Chat-{uuid.uuid4().hex[:6]}"
        st.session_state.messages = []
        st.rerun()

    st.divider()

    threads = get_threads()

    for thread in threads:

        col1, col2 = st.columns([4, 1])

        # LOAD THREAD
        with col1:
            if st.button(
                thread,
                key=f"thread_{thread}",
                use_container_width=True
            ):
                st.session_state.thread_name = thread

                data = get_thread_messages(thread)

                st.session_state.messages = [
                    {
                        "role": role,
                        "content": msg
                    }
                    for role, msg in data
                ]

                st.rerun()

        # DELETE BUTTON
        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{thread}"
            ):
                st.session_state.delete_confirm_thread = thread

    # =========================
    # DELETE CONFIRMATION MODAL
    # =========================

    if st.session_state.delete_confirm_thread:

        st.warning(
            f"Are you sure you want to delete "
            f"'{st.session_state.delete_confirm_thread}' chat?"
        )

        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button(
                "✅ Yes Delete",
                use_container_width=True
            ):

                delete_thread(
                    st.session_state.delete_confirm_thread
                )

                st.session_state.delete_confirm_thread = None

                st.success("Chat deleted successfully.")

                st.rerun()

        with col_no:
            if st.button(
                "❌ Cancel",
                use_container_width=True
            ):

                st.session_state.delete_confirm_thread = None

                st.rerun()


# =========================
# MAIN TITLE
# =========================

st.title("🌾 Farmer AI Assistant")


# =========================
# DISPLAY CHAT
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# USER INPUT
# =========================

user_input = st.chat_input(
    "Ask farming related question..."
)


if user_input:

    # USER MESSAGE
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    save_message(
        st.session_state.thread_name,
        "user",
        user_input
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # =========================
    # ASSISTANT RESPONSE
    # =========================

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        # STREAMING GRAPH
        for chunk in farmer_graph.stream(
            {
                "question": user_input
            }
        ):

            # FINAL ANSWER NODE
            if "response" in chunk:

                node_data = chunk["response"]

                if "answer" in node_data:

                    full_response += node_data["answer"]

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # REJECT NODE
            if "reject" in chunk:

                node_data = chunk["reject"]

                if "answer" in node_data:

                    full_response += node_data["answer"]

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

        response_placeholder.markdown(full_response)

    # SAVE ASSISTANT MESSAGE
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    save_message(
        st.session_state.thread_name,
        "assistant",
        full_response
    )
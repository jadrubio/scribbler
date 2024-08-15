import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory

def setup_memory():
    if 'run_id' not in st.session_state:
        st.session_state['run_id'] = None
    if 'agentState' not in st.session_state:
        st.session_state['agentState'] = "start"
    if 'consent' not in st.session_state:
        st.session_state['consent'] = False
    if 'exp_data' not in st.session_state:
        st.session_state['exp_data'] = True
    if 'llm_model' not in st.session_state:
        st.session_state.llm_model = "gpt-4o"
    st.session_state.memory = ConversationBufferMemory(memory_key="history", chat_memory=StreamlitChatMessageHistory(key="langchain_messages"))

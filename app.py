from config import initialize_env
from memory.memory_manager import setup_memory
from data_collection.data_collector import getData
from feedback.feedback_manager import collectFeedback, summariseData

import streamlit as st

initialize_env()

st.set_page_config(page_title="Study bot", page_icon="📖")
st.title("📖 Study bot")

setup_memory()

if st.session_state['agentState'] == "start":
    getData()
elif st.session_state['agentState'] == "summarise":
    summariseData()

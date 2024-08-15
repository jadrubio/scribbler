import os
import streamlit as st

def initialize_env():
    os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']
    os.environ["LANGCHAIN_API_KEY"] = st.secrets['LANGCHAIN_API_KEY']
    os.environ["LANGCHAIN_PROJECT"] = st.secrets['LANGCHAIN_PROJECT']
    os.environ["LANGCHAIN_TRACING_V2"] = 'true'

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Faculty Recommender AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Read the HTML file
html_file = Path("app/static/index.html").read_text(encoding="utf-8")

# Render the HTML component
st.components.v1.html(
    html_file,
    height=900,
    scrolling=True
)
import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

html_file = Path("app/static/index.html").read_text(encoding="utf-8")

st.components.v1.html(
    html_file,
    height=800,
    scrolling=True
)
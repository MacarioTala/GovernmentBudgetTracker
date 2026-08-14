
import streamlit as st


def load_css_for_streamlit_controls(filename):
    with open(filename) as f:
        st.html(f"<style>{f.read()}</style>")


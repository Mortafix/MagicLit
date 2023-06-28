import streamlit as st
from utils.components.html import spacer, title


def show(**kwargs):
    title(st, 1, "Admin Panel", "admin_panel_settings")
    st.info("This page is reserved to **super** user (or admin)")
    spacer(1)
    st.json(st.session_state.user)

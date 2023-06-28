from re import search

import streamlit as st


def st_user():
    return st.session_state.get("user", {}) or dict()


def change_page(page, skip_clear=False):
    st.session_state["current-page"] = page
    if skip_clear:
        skip_clear_session()
        st.session_state["auto-change-page"] = True
    st.session_state["skip"] = True
    st.session_state["page-changed"] = True
    st.experimental_rerun()


def skip_clear_session():
    st.session_state["skip-change-page"] = True


def session_on_change_page():
    if st.session_state.pop("skip-change-page", False):
        return
    keys_to_not_clear = [
        "user",
        "current-page",
        "redirect-page",
        "main-refresh",
        "last-refresh",
        "skip",
        "last-fragment",
        "script",
        "clienti",
    ]
    if st.session_state.pop("change-same-section", False):
        keys_to_not_clear.extend(["filters", "flt-mode"])
    for key in st.session_state:
        if key not in keys_to_not_clear or search(r"^cache-", key):
            st.session_state.pop(key, None)


def set_direct_page_link(menu, params):
    if page := params.get("page"):
        page_url = page[0]
        if menu.get(page_url):
            st.session_state["direct-page"] = page_url

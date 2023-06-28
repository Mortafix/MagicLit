import streamlit as st
from utils.components.html import div, icon


def continue_insert_form(success_message, component=st):
    if st.session_state.get("form-sent"):
        sent_form = component.form("form-again")
        sent_form.success(success_message, icon="✅")
        if sent_form.form_submit_button("Insert again ➡️", use_container_width=True):
            st.session_state.pop("form-sent")
            st.experimental_rerun()
        return True
    return False


def multiple_form_items(data, section, sel_idx, icon_name, field, key, component=st):
    text = str()
    for i, entry in enumerate(data.get(key) or []):
        h_params = f"@sec={section}&sub={key}&index={i}"
        trasp = f"<span>{icon(icon_name)}{entry.get(field)}</span>"
        span_html = f"<a href='#edit{h_params}'>{trasp}</a>"
        a_rem = f"<a class='ic' href='#rem{h_params}'>{icon('clear')}</a>"
        active_class = "active" if i == sel_idx else ""
        a_mv = f"<a class='ic blue' href='#mov{h_params}'>{icon('arrow_right_alt')}</a>"
        div_content = f"{span_html}{a_mv if i +1  != len(data.get(key)) else ''}{a_rem}"
        text += f"<div class='item {active_class}'>{div_content}</div>"
    div(component, "multiple-items", text)

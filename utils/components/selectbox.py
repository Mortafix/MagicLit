import streamlit as st

# ---- Main


def smart_select(
    component,
    elements,
    label,
    base_element="",
    base_fmt=lambda id, el: el,
    selected=None,
    filters=None,
    key=None,
    empty=False,
    add_fmt="",
    multi=False,
    sort=None,
    hide_if_empty=False,
    **kwargs,
):
    if hide_if_empty and not elements:
        return None
    if sort:
        elements = {elem: elements.get(elem) for elem in sort}
    current_page = st.session_state.get("current-page", "page")
    base_key = f"{current_page}-{(label or label).replace(' ', '_')}"
    key = base_key + (f"-{key}" if key else "")
    idx = 0
    if not multi and selected in elements:
        idx = list(elements).index(selected) + (1 if empty else 0)
    if multi and selected:
        selected = [el for el in selected if el in elements]
    el_list = {**({"": base_element} if empty else dict()), **elements}
    fmt_func = lambda x: base_fmt(x, el_list.get(x)) + (add_fmt and add_fmt(x))
    st_func = component.multiselect if multi else component.selectbox
    selection = {"default": selected} if multi else {"index": idx}
    return st_func(label, el_list, format_func=fmt_func, key=key, **selection, **kwargs)


# ---- Specific


def hello_select(component, label, **kwargs):
    choices = {0: "Ciao", 1: "Hello", 2: "Hola", 3: "Salut"}
    return smart_select(component, choices, label, **kwargs)


def sex_select(component, **kwargs):
    choices = {"M": "Male", "F": "Female"}
    return smart_select(component, choices, "Sex", **kwargs)

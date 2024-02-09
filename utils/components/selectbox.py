import streamlit as st

# ---- Main


def smart_select(
    component,
    elements,
    label,
    base_fmt=lambda id, el: el,
    selected=None,
    filters=None,
    key=None,
    empty=False,
    add_fmt="",
    multi=False,
    sort=None,
    hide_if_empty=False,
    placeholder=None,
    **kwargs,
):
    if hide_if_empty and not elements:
        return None
    if sort:
        elements = {elem: elements.get(elem) for elem in sort}
    elements = {el: val for el, val in elements.items() if not filters or el in filters}
    current_page = st.session_state.get("current-page", "page")
    base_key = f"{current_page}-{(label or label).replace(' ', '_')}"
    key = base_key + (f"-{key}" if key else "")
    idx = None if empty else 0
    if not multi and selected in elements:
        idx = list(elements).index(selected)
    if multi and selected:
        selected = [el for el in selected if el in elements]
    fmt_func = lambda x: base_fmt(x, elements.get(x)) + (add_fmt and add_fmt(x))
    st_func = component.multiselect if multi else component.selectbox
    selection = {"default": selected} if multi else {"index": idx}
    return st_func(
        label,
        elements,
        format_func=fmt_func,
        key=key,
        placeholder=placeholder or f"Seleziona {label}",
        **selection,
        **kwargs,
    )


# ---- Specific


def hello_select(component, label, **kwargs):
    choices = {0: "Ciao", 1: "Hello", 2: "Hola", 3: "Salut"}
    return smart_select(component, choices, label, **kwargs)


def sex_select(component, **kwargs):
    choices = {"M": "Male", "F": "Female"}
    return smart_select(component, choices, "Sex", **kwargs)

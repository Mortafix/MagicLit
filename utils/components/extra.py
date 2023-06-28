from datetime import datetime, timedelta

import streamlit as st
from utils.components.html import div, icon


def date_selector(key, step=1, date_fmt="%d %b %y", monday=False, component=st):
    today = datetime.today()
    start_d = today - timedelta(days=today.weekday() if monday else 0)
    offset = st.session_state.get(f"date-{key}", 0)
    start_d += timedelta(days=step) * offset
    end_d = start_d + timedelta(days=step - 1)
    # html
    dates_label = f"{start_d:{date_fmt}}"
    if start_d != end_d:
        dates_label += f"{icon('trending_flat')}{end_d:{date_fmt}}"
    arrow_back = f"<a href='#date_{key}@direction=-1'>{icon('navigate_before')}</a>"
    arrow_next = f"<a href='#date_{key}@direction=1'>{icon('navigate_next')}</a>"
    oggi = f"<span class='today'><a href='#date_{key}@direction=0'>TODAY</a></span>"
    text = f"<div class='dates'>{arrow_back}{dates_label}{arrow_next}{oggi}</div>"
    div(component, "date-selector", text)
    return start_d


def cards_display(data, main, top, i_name, icons=None, sub_f=None, tags_f=None, cmp=st):
    text = str()
    for entry in data:
        e_id = entry.get("id")
        disabled = "disabled" if entry.get("disabled", False) else ""
        main_val = (
            entry.get(main, "")
            if isinstance(main, str)
            else " ".join(entry.get(attr, "") for attr in main or [])
        )
        top_val = (
            entry.get(top, "")
            if isinstance(top, str)
            else " ".join(entry.get(attr) for attr in top or [])
        )
        sub_f = sub_f or (lambda x: "")
        tags_f = tags_f or (lambda x: "")
        span_html = (
            f"<span class='top'>{top_val}</span><span class='main'>{main_val}</span>"
            f"<span class='tags'>{tags_f(entry)}</span>"
            f"<span class='sub'>{sub_f(entry)}</span>"
        )
        view_icons = [
            icon
            for icon in icons or []
            if not icon[0].endswith("bilita")
            or (icon[0] == "Disabilita" and not disabled)
            or (icon[0] == "Abilita" and disabled)
        ]
        icons_html = "".join(
            f"<a href='#{url}@id={e_id}'>{label}{icon(icon_name)}</a>"
            for label, url, icon_name in view_icons or []
        )
        icons_html = (
            f"<div class='icons'>{icon('more_horiz')}<span>{icons_html}</span></div>"
        )
        if not icons:
            icons_html = ""
        card = f"{icon(i_name)}{span_html}"
        text += f"<div class='card {disabled}'>{card}{icons_html}</div>"
    div(cmp, "cards", text)


def mini_cards_display(data, attribute, icon_name=None, default=None, component=st):
    text = str()
    for entry in data:
        main_text = entry.get(attribute, default)
        icon_html = icon(icon_name) if icon_name else ""
        text += f"<div class='card mini'>{icon_html}<span>{main_text}</span></div>"
    div(component, "cards", text)


def progress_bar(bars, current, total, component=st):
    text = str()
    l_space = 0
    for i, (label, bar) in enumerate(bars.items(), 1):
        bar_styles = {
            "width": f"{min(bar, 100-l_space):.3f}%",
            "left": f"{l_space:.3f}%",
            "background-color": f"var(--rainbow-{i})",
            "outline-color": f"var(--rainbow-{i})",
        }
        bar_style = "; ".join(f"{attr}:{val}" for attr, val in bar_styles.items())
        text += f"<span style='{bar_style}'><label>{label}</label></span>"
        l_space = min(l_space + bar, 100)
        if l_space >= 100:
            break
    text += f"<div class='current' style='width:{max(l_space, 1)}%'>{current}</div>"
    text += f"<div class='total'>{total}</div>"
    div(component, "progress-bar", text)

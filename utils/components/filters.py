from datetime import datetime

import streamlit as st
from utils.components.html import div, icon


def common_filters(filters, current, component=st):
    filters = [values if len(values) == 4 else (*values, None) for values in filters]
    text = str()
    for icon_name, title, url, badge in filters:
        span_html = "" if not title else f"<span>{title}</span>"
        a_html = f"<a href='#flt@mode={url}'>{icon(icon_name)}{span_html}</a>"
        is_active = current != "no" and str(current) == str(url)
        d_class = "flt mirror" + (" flt-active" if is_active else "")
        text += f"<div class='{d_class}'>{a_html}"
        if badge:
            text += f"<span>{badge}</span>"
        text += "</div>"
    text = f"<div class='common-filters'>{text}</div>"
    div(component, "wrapper-filters", text)


def to_datetime(date, time=False):
    now = datetime.now()
    hour, minute = (now.hour, now.minute) if time else (0, 0)
    if not date:
        return None
    if isinstance(date, str):
        return datetime(*map(int, date.split(".")[::-1]), hour, minute)
    if isinstance(date, datetime):
        return date
    return datetime(date.year, date.month, date.day, hour, minute)


def check_filtri(data, filters, types=None):
    if not filters:
        return True
    types = types or dict()
    for index, value in filters.items():
        # index not in table
        if index > len(data):
            return True
        # filters unset
        if value in (None, "", (datetime.min, datetime.max), []):
            continue
        # filters set
        if type(flt := types.get(index)) is tuple and (not flt[0] or flt[0] == value):
            if flt[1](value, data[index]):
                return False
        elif types.get(index) == "list":
            if data[index] not in value:
                return False
        elif types.get(index) == "date-range":
            date = to_datetime(data[index])
            if not (date and value[0] <= date <= value[1]):
                return False
        elif types.get(index) == "substr":
            if value not in data[index]:
                return False
        elif types.get(index) == "comma-list":
            table_values = [val.strip() for val in data[index].split(",")]
            if not any(val in table_values for val in value):
                return False
        # general
        elif index >= len(data):
            return True
        elif data[index] != value:
            return False
    return True

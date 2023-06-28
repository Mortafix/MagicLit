from math import ceil

import streamlit as st
from utils.components.html import div, h2, icon, spacer


def table(
    title,
    data,
    stats=None,
    funcs=None,
    exclude=False,
    sorts=None,
    widths=None,
    all_pages=False,
    component=st,
):
    page_max_row = 10 if not all_pages else -1
    funcs, sorts, widths = funcs or list(), sorts or dict(), widths or dict()
    header, data = data[0], data[1:]
    indexes = [i for i, field in enumerate(header) if field not in (exclude or [])]
    total_col = len(indexes)
    total_row = len(data)
    total_pages = ceil(total_row / page_max_row)
    page = p if (p := st.session_state.get("page")) is not None else 1
    page = max(min(total_pages, page), 0)
    st.session_state.page = page
    label_sorts = {real_sort: label for label, real_sort in sorts.items()}
    active_sort = (
        {label_sorts.get(sort[0], sort[0]): "south" if sort[1] else "north"}
        if (sort := st.session_state.get("sort-table"))
        else dict()
    )
    head_labels = "".join(
        f"<th width='{widths.get(i, 'auto')}'>"
        f"<a href='#sort@val={sorts.get(label, label)}'>{label}</a>"
        f"{icon(icon_name) if (icon_name := active_sort.get(label)) else ''}</th>"
        for i in indexes
        if (label := header[i])
    )
    if funcs:
        head_labels += "<th width='40px'></th>"
    title_table = f"<th colspan={total_col + (1 if funcs else 0)}>{title}</th>"
    rows = f"<thead><tr class='title'>{title_table}</tr><tr>{head_labels}</tr></thead>"
    start_index = (page - 1) * page_max_row
    data = (
        data[start_index : start_index + page_max_row]
        if page_max_row > 0 and page > 0
        else data
    )

    def cell_value(value):
        if not isinstance(value, tuple):
            return value
        value, descr = value
        if not descr:
            return value
        return f"{value}<p>{descr}</p>"

    values = "".join(
        "<tr>"
        + "".join(f"<td>{cell_value(row[i])}</td>" for i in indexes)
        + _build_table_funcs(funcs, header, row)
        + "</tr>"
        for row in data
    )
    if stats:
        total_col += 1
        stats = "".join(
            f"<td>{icon(func[1], size=18)} {func[0]([r[i] for r in data])}</td>"
            if (func := stats.get(i))
            else "<td></td>"
            for i in indexes + [None] * (1 if funcs else 0)
        )
        values += f"<tr class='stats-row'>{stats}</tr>"
    pages = str()
    if page_max_row > -1:
        t_page, t_total = page, total_pages
        func_icon, func_name, func_desc = (
            ("more_horiz", "single", "Show less")
            if page == 0
            else ("menu", "all", "Show all")
        )
        arrow_l = f"<a href='#table@page=left'>{icon('chevron_left')}</a>"
        arrow_r = f"<a href='#table@page=right'>{icon('chevron_right')}</a>"
        if page == 0:
            arrow_l, arrow_r = "", ""
            t_page, t_total = 1, 1
        pages = (
            f"<a href='#table@page={func_name}'><span>{icon(func_icon)}"
            f"<desc>{func_desc}</desc></span></a>"
            f"<span>{arrow_l}<b>{t_page}</b> di <b>{t_total}</b>{arrow_r}</span>"
        )
    values += f"<tr class='pages'><td colspan='{total_col}'>{pages}</td></tr>"
    rows += f"<tbody>{values}</tbody>"
    spacer(1.5)
    div(component, "table-container", f"<table>{rows}</table>")
    return [[header[i] for i in indexes]] + [[row[i] for i in indexes] for row in data]


def _build_table_funcs(funcs, header, row):
    if not funcs:
        return ""

    def single(icon_name, func, fields, descrizione, visible):
        if visible is not True:
            if not visible(*[row[header.index(field)] for field in fields]):
                return ""
        sanitize = lambda label: label.split()[0][:5].lower()
        other = [f"{sanitize(field)}={row[header.index(field)]}" for field in fields]
        url = f"#{func}@{'&'.join(other)}"
        span = f"<span>{descrizione}</span>"
        return f"<a href='{url}'>{icon(icon_name, other_class='table-btn')}{span}</a>"

    funcs = [(values) if len(values) == 5 else (*values, True) for values in funcs]
    icons = "".join(single(*values) for values in funcs)
    func_container = f"<span class='funcs'>{icons}</span>{icon('more_vert')}"
    return f"<td class='funcs-col'><span class='container'>{func_container}</span></td>"


# ---- paging and sort


def change_table_page(page):
    if page == "all":
        st.session_state.page = 0
        return
    if page == "single":
        st.session_state.page = 1
        return
    current_page = st.session_state.get("page", 1)
    direction = -1 if page == "left" else 1
    if current_page == 1 and direction < 0:
        return
    st.session_state.page = current_page + direction


def change_table_sort(val):
    prev_sort, prev_direction = st.session_state.pop("sort-table", (None, None))
    direction = False
    if prev_sort == val:
        if prev_direction is True:
            return st.session_state.pop("sort-table", None)
        direction = True
    st.session_state["sort-table"] = val, direction


# ---- report


def csv_report(data, page, funcs=None, title="Recap", component=st):
    header, *real_data = data
    proc_data = [
        [funcs.get(i, lambda x: x)(val) if funcs else val for i, val in enumerate(row)]
        for row in real_data
    ]
    text_data = "\n".join(";".join(map(str, row)) for row in [header] + proc_data)
    h2(component, title, "content_paste_search")
    filename = f"SuperStreamlit_{page.title()}.csv"
    component.download_button(
        "Download **Excel** 🗄",
        text_data,
        filename,
        mime="text/csv",
        use_container_width=True,
    )

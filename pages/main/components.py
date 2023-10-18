from csv import reader
from datetime import datetime
from functools import partial
from os import path

import streamlit as st
from utils.components.elements import (Attribute, CombinedAttribute,
                                       ListAttribute, SubAttribute, display)
from utils.components.extra import (cards_display, date_selector,
                                    mini_cards_display, progress_bar)
from utils.components.filters import check_filtri, common_filters
from utils.components.form import continue_insert_form, multiple_form_items
from utils.components.html import Notification, h2, h4, spacer, title
from utils.components.selectbox import hello_select, sex_select
from utils.components.table import (change_table_page, change_table_sort,
                                    csv_report, table)
from utils.web.fragment import manage_fragment, skip_fragment

# ---- UTILS


def remove_item(sec, sub, index):
    if len(st.session_state[sec]["elements"]) > int(index):
        st.session_state[sec]["elements"].pop(int(index))
        st.session_state.pop("edit-extra", None)


def edit_item(sec, sub, index):
    st.session_state.pop("edit-extra", None)
    st.session_state["edit-extra"] = int(index)


def move_item(sec, sub, index):
    idx = int(index)
    if len(st.session_state[sec]["elements"]) > idx + 1:
        items = st.session_state[sec]["elements"]
        items[idx + 1], items[idx] = items[idx], items[idx + 1]
        st.session_state[sec]["elements"] = items


@st.cache_data
def get_table_data():
    with open(path.join(st.secrets.script.folder, "static/data/characters.csv")) as f:
        return [
            (int(idc), name, int(age), sex, int(year), key)
            for idc, name, age, sex, year, key in reader(f)
        ]


def fake_delete(id):
    Notification("Entry **deleted**! (not really in this example)").success()


def change_date(attribute, direction):
    direction = int(direction)
    offset = st.session_state.get(f"date-{attribute}", 0)
    offset += direction
    if not direction:
        offset = 0
    st.session_state[f"date-{attribute}"] = offset


# ---- PAGES


def element(**kwargs):
    title(st, 1, "Elements", "dashboard")
    st.info(
        "Simple **information displayer** `(Utils > Components > Elements)`", icon="ℹ️"
    )
    spacer(2)
    data = {
        "name": "Luigi",
        "year": 1985,
        "console": {"NES": 1983, "Switch": 2017},
        "princesses": ["Peach", "Daisy", "Rosalinda"],
        "price": 349,
        "currency": "$",
    }
    attributes = [
        Attribute("name"),
        Attribute("year", "Age", func=lambda x: datetime.today().year - x),
        SubAttribute(
            "console",
            attributes=[Attribute("NES"), Attribute("Switch")],
        ),
        ListAttribute(
            "princesses",
            single=Attribute(func=lambda x: f"Princess {x}"),
        ),
        CombinedAttribute(
            ["price", "currency"],
            "price",
        ),
    ]
    display(data, attributes)


def form(**kwargs):
    title(st, 1, "Forms", "checklist")
    st.info("Simple **form** `(Utils > Components > Form)`", icon="ℹ️")

    # fragment
    fragment = kwargs.get("fragment")
    params_funcs = {
        "rem": remove_item,
        "mov": move_item,
        "edit": edit_item,
    }
    manage_fragment(params_funcs, fragment)

    # multiple insert check
    if continue_insert_form("**Entry** added succesfully!"):
        st.session_state.pop("extra-info", None)
        return

    # app
    c_form = st.form("simple-form")
    data = dict()
    h4(c_form, "General", "person")
    cols = c_form.columns(3)
    data["name"] = cols[0].text_input("Name", placeholder="Name")
    data["surname"] = cols[1].text_input("Surname", placeholder="Surname")
    data["age"] = cols[2].number_input("Age", min_value=18, max_value=99, step=1)
    data["notes"] = c_form.text_area("Notes", placeholder="Optional notes")
    # extra
    h4(c_form, "Extra", "info")
    extra_info = st.session_state.get("extra-info", {})
    selected_idx = st.session_state.get("edit-extra", None)
    corr_extra = extra_info.get("elements", [])
    is_editing = selected_idx is not None
    extra_selected = corr_extra[selected_idx] if is_editing else dict()
    multiple_form_items(
        extra_info,
        "extra-info",
        selected_idx,  # current selected
        "lightbulb_circle",  # icon
        "category",  # attribute displayed
        "elements",
        c_form,
    )
    cols = c_form.columns((2, 3))
    f_sezione = cols[0].text_input(
        "Category", extra_selected.get("category", ""), placeholder="Extra category"
    )
    f_correzione = cols[1].text_input(
        "Value", extra_selected.get("value", ""), placeholder="Extra value"
    )
    verb_btn = "Edit" if is_editing else "Add"
    if c_form.form_submit_button(f"{verb_btn} **extra** ➕", use_container_width=True):
        skip_fragment()
        selected_idx = st.session_state.pop("edit-extra", None)
        if f_sezione and f_correzione:
            if is_editing:
                corr_extra.pop(selected_idx)
            if not st.session_state.get("extra-info"):
                st.session_state["extra-info"] = dict()
            data = {"category": f_sezione, "value": f_correzione}
            new_data = corr_extra + [data]
            st.session_state["extra-info"]["elements"] = new_data
        st.rerun()
    data["Others"] = c_form.text_input("Others", placeholder="Other relevant info")

    # form sumbit
    if c_form.form_submit_button("Send ✅", use_container_width=True):
        if not data.get("name"):
            return st.warning("**Name** is required!", icon="⚠️")
        if not extra_info.get("elements"):
            return st.warning("Insert at least one **extra**", icon="⚠️")
        if True:  # do something
            st.session_state["form-sent"] = True
            st.rerun()


def titles(**kwargs):
    title(st, 1, "Titles", "text_fields")
    st.info("Simple **titles** with _icons_ `(Utils > Components > Html)`", icon="ℹ️")

    title(st, 1, "Title h1", "rtt")
    st.code("# title(component, size, text, icon)\ntitle(st, 1, 'Title h1', 'rtt')")
    spacer(1)

    h2(st, "Title h2", "hdr_auto")
    st.code("# h2(component, text, icon)\nh2(st, 'Title h2', 'hdr_auto')")
    spacer(1)

    h4(st, "Title h4", "sort_by_alpha")
    st.code("# h4(component, text, icon)\nh4(st, 'Title h4', 'sort_by_alpha')")


def notification(**kwargs):
    title(st, 1, "Notifications", "text_fields")
    st.info("**Notifications** system `(Utils > Components > Html)`", icon="ℹ️")
    spacer(1)

    if st.button("Success ✅", key="success"):
        Notification("This is a **success** notification").success()
    spacer(1)

    if st.button("Warning ⚠️", key="warning"):
        Notification("This is a **warning** notification").warning()
    spacer(1)

    if st.button("Error ⛔️", key="error"):
        Notification("This is an **erroro** notification").error()
    spacer(1)

    if st.button("Info ℹ️", key="info"):
        Notification("This is an **info** notification").info()
    spacer(1)

    if st.button("Custom 🔮", key="custom"):
        Notification("This is a **custom** notification").custom(
            "auto_awesome", "#b28ef9"
        )
    spacer(1)

    if st.button("Toast 🥪", key="toast"):
        st.toast("This is a _Streamlit_ **toast**!", icon="👋🏻")


def selectbox(**kwargs):
    title(st, 1, "Selectboxes", "check_box")
    st.info("Expand **selectbox** in form `(Utils > Components > Seletbox)`", icon="ℹ️")
    spacer(1)

    select_form = st.form("selects")
    hello_select(select_form, "Simple selection", key="simple")
    hello_select(
        select_form,
        "Options with format",
        base_fmt=lambda k, v: f"{v} ({k})",
        add_fmt=lambda x: f" [add {x+2}]",
        key="base",
    )
    hello_select(
        select_form,
        "Option selected and empty value",
        selected=2,
        empty=True,
        key="selected",
    )
    hello_select(select_form, "Multiselect", multi=True)
    select_form.form_submit_button("Save ✅", use_container_width=True)


def tables(**kwargs):
    title(st, 1, "Tables", "table_chart")
    st.info("Advanced **tables** `(Utils > Components > Table)`", icon="ℹ️")
    spacer(1)

    FIELDS = ["ID", "Name", "Age", "Sex", "Year", "hash"]

    # fast filters function
    def add_filters(mode):
        st.session_state["page"] = 1
        filters = dict()
        if mode == "female":
            filters = {FIELDS.index("Sex"): "F"}
        if mode == "young":
            filters = {FIELDS.index("Age"): range(16)}
        st.session_state["filters"] = filters
        st.session_state["flt-mode"] = mode

    # fragment
    fragment = kwargs.get("fragment")
    params_funcs = {
        "table": change_table_page,
        "sort": change_table_sort,
        "flt": add_filters,
        "del": fake_delete,
    }
    manage_fragment(params_funcs, fragment)

    # data
    raw_data = get_table_data()
    sort, reverse = st.session_state.get("sort-table", (None, False))
    sorts = ([FIELDS.index(sort)] if sort else []) + [1]
    raw_data.sort(key=lambda el: [el[i] for i in sorts], reverse=reverse)

    # filters form
    _, fast_filter_col = st.columns((1, 2))
    filter_expander = st.expander("Advanced **filters**")
    filter_form = filter_expander.form("filtri")
    cols = filter_form.columns(4)
    f_name = cols[0].selectbox(
        "Name",
        sorted([row[1] for row in raw_data]),
        index=None,
        placeholder="Select name",
    )
    f_sex = sex_select(cols[1], empty=True)
    f_ages = cols[2].slider("Age", value=(0, 1000), step=1)
    if cols[3].form_submit_button("Filter ✅", use_container_width=True):
        filters = {
            FIELDS.index("Name"): f_name,
            FIELDS.index("Sex"): f_sex,
            FIELDS.index("Age"): range(f_ages[0], f_ages[1] + 1),
        }
        st.session_state["filters"] = filters
        st.session_state["flt-mode"] = "off"
    if cols[3].form_submit_button("Clear ❌", use_container_width=True):
        st.session_state["filters"] = None
    flts = st.session_state.get("filters")

    # fast filters
    curr_mode = st.session_state.get("flt-mode")
    fast_filters = [
        ("female", "Female", "female"),
        ("child_friendly", "Young", "young"),
        ("highlight_off", None, "no"),
    ]
    common_filters(fast_filters, curr_mode, component=fast_filter_col)

    # table
    filters_funcs = {"Age": "list"}
    types = {FIELDS.index(label): func for label, func in filters_funcs.items()}
    data = [FIELDS] + [row for row in raw_data if check_filtri(row, flts, types)]
    stats = {FIELDS.index("ID"): (len, "playlist_add_check_circle")}
    funcs = [("delete_forever", "del", ["ID"], "Delete")]
    exclude = ["hash"]
    sorts = {"ID": "ID"}  # use to map field sorting to another
    widths = {FIELDS.index("Name"): "30%"}
    table_data = table(
        "Nintendo Characters", data, stats, funcs, exclude, sorts, widths
    )

    # csv report
    side_section = st.sidebar.container()
    funcs = {3: lambda x: {"M": "Male", "F": "Female"}.get(x)}
    csv_report(table_data, "nintendo_characters", funcs, component=side_section)


def extra(**kwargs):
    title(st, 1, "Extra", "area_chart")
    st.info("Mixed extra **components** `(Utils > Components > Extra)`", icon="ℹ️")
    spacer(1)

    # fragment
    fragment = kwargs.get("fragment")
    params_funcs = {
        "date_simple": partial(change_date, "simple"),
        "date_range": partial(change_date, "range"),
        "date_week": partial(change_date, "week"),
    }
    manage_fragment(params_funcs, fragment)

    # date changer
    h2(st, "Date selectors", "date_range")
    date_selector("simple")
    spacer(2)
    date_selector("range", step=30)
    spacer(2)
    date_selector("week", step=7, date_fmt="%A %d %B", monday=True)
    spacer(2)

    # cards displayer
    h2(st, "Card displayer", "loyalty")
    data = [
        {"name": "Mario", "game": "Super Mario Bros"},
        {"name": "Link", "game": "The Legend of Zelda"},
        {"name": "Samus Aran", "game": "Metroid"},
        {"name": "Donkey Kong", "game": "Donkey Kong"},
    ]
    cards_display(data, "name", "game", "sports_esports")
    spacer(1)
    mini_cards_display(data, "name", "videogame_asset")
    spacer(1)

    # multi progress bar
    h2(st, "Progress bar", "stacked_bar_chart")
    data = {
        "Super Mario Bros": 25,
        "The Legend of Zelda": 15,
        "Metroid": 10,
        "Donkey Kong": 8,
        "Pokémon": 12,
        "Kirby's Dream Land": 5,
        "Star Fox": 4,
        "F-Zero": 3,
    }
    progress_bar(data, sum(data.values()), 100, component=st)

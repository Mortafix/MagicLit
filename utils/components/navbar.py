import streamlit as st
from utils.components.html import div, icon
from utils.components.page import st_user
from utils.platform.user import get_username, is_superadmin
from utils.web.fragment import skip_fragment, split_fragment


def navbar(menu, current_page, logo):
    def submenu(pages):
        soon = f"<span>Coming soon {icon('flight')}</span>"
        url = lambda page: "#" if page.developing else f"#url@page={page.url}"
        submenu_pages = "".join(
            f"<li class='{'dev' if page.developing else ''}'><a href='{url(page)}'>"
            f"{icon(page.icon)}{page.title}{soon if page.developing else ''}</a></li>"
            for page in pages
            if not page.hidden
        )
        return f"<div class='submenu'><ul>{submenu_pages}</ul></div>"

    # pages
    pages = "".join(
        f"<div class='dropdown {'active' if page.contains(current_page) else ''}'>"
        f"<a class='snake' href='#{f'url@page={page.url}' if page.url else ''}'>"
        f"{page.title}</a>{submenu(page.pages)}</div>"
        for page in menu.pages
        if not page.hidden and not page.super_admin or is_superadmin()
    )
    # user
    user = st_user()
    user_html = (
        f"<div class='nickname mirror'><a class='login' href='#url@page=profile'>"
        f"{icon('person')}<span>{get_username(user)}</span></a></div>"
    )
    # company
    azienda = f"<a href='#'>{icon('business')}<span>Nintendo Inc.</span></a>"
    azienda_html = f"<div class='azienda'>{azienda}</div>"
    # icons
    total_noti = 3
    fast_icons = {
        "code": "https://github.com/Mortafix/magiclit",
        "notifications": "#url@page=profile-notifications",
        "settings": "#url@page=profile-settings",
        "logout": "#logout@c=1",
    }
    badge_visibile = lambda name: name == "notifications" and total_noti > 0
    icons = "".join(
        f"<a href='{url}'>{icon(icon_name, other_class=icon_name)}"
        f"<span class='{'noti-n' if badge_visibile(icon_name) else 'empty'}'>"
        f"{total_noti}</span></a>"
        for icon_name, url in fast_icons.items()
    )
    menu_mobile = f"<span class='menu-container'>{icon('menu')}</span>"
    # complete
    navbar_html = (
        f"<img src='{logo}'>{menu_mobile}<ul>{pages}</ul><div class='user'>{user_html}"
        f"{azienda_html}</div><div class='icons'>{icons}</div>"
    )
    return div(st, "navbar-container", f"<nav class='navbar'>{navbar_html}</nav>")


def page_selector(current_fragment, menu):
    is_changed = False
    mode, params = split_fragment(current_fragment)
    if not (current_page := st.session_state.get("current-page")):
        current_page = st.session_state.pop("direct-page", None) or menu.first.url
        st.session_state["current-page"] = current_page
    page_selected = params.get("page")
    is_login = st.session_state.pop("is_login", False)
    if not is_login and mode == "logout":
        st.session_state.clear()
        skip_fragment()
        st.experimental_rerun()
    if mode == "url" and page_selected and page_selected != current_page:
        page_changed = st.session_state.pop("page-changed", None)
        different_fragment = current_fragment != st.session_state.get("last-fragment")
        if different_fragment or not page_changed:
            if page_selected.split("-")[0] == current_page.split("-")[0]:
                st.session_state["change-same-section"] = True
            is_changed = True
            st.session_state["current-page"] = page_selected
            st.session_state["redirect-page"] = menu.get(page_selected).redirect
            st.session_state["last-fragment"] = current_fragment
            current_page = page_selected
    elif st.session_state.get("page-changed"):
        current_page = st.session_state.get("current-page")
        st.session_state["redirect-page"] = menu.get(current_page).redirect
    return current_page, is_changed

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_url_fragment import get_fragment
from utils.components.html import (image, login_css, multiple_local_css,
                                   remote_css, remove_streamlit_menu, spacer,
                                   special_css)
from utils.components.navbar import navbar, page_selector
from utils.components.page import (session_on_change_page,
                                   set_direct_page_link, st_user)
from utils.menu.menu import app_menu
from utils.platform.extra import get_version
from utils.platform.user import check_login
from utils.web.fragment import skip_fragment

st.set_page_config(
    page_title="Magiclit",
    page_icon="app/static/images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main(fragment, static_attr):

    # This is the custom user I used to auth in the app
    user = st_user()

    # I automatically refresh the page every 2 minutes [OPTIONAL]
    st_autorefresh(interval=2 * 60 * 1000, key="main-refresh")

    # ---- STYLE
    # local CSS: main style - version number is used to ensure that the client
    #   browser automatically refreshes the CSS
    # remote CSS: additional style - in this case Material Icons from Google
    # Streamlit:  removed Streamlit default hamburger menu [OPTIONAL]
    multiple_local_css(get_version())
    remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
    remove_streamlit_menu()

    # ---- LOGIN
    if not user:
        # custom login CSS and LOGO
        login_css(get_version())
        image("app/static/images/logo.png", "logo")

        # simple login form
        login_form = st.form("login-form", clear_on_submit=True)
        login_form.info("Put **any information** you want to login!", icon="ℹ️")
        username = login_form.text_input("Mail", placeholder="Mail")
        password = login_form.text_input(
            "Password",
            type="password",
            placeholder="Password",
            autocomplete="current-password",
        )
        if login_form.form_submit_button("Login 👤", use_container_width=True):
            if check_login(username, password, component=login_form):
                skip_fragment()
                st.rerun()
        return

    # ---- MENU
    # this is how the menu and all the pages are managed within the app.
    current_page, is_page_changed = page_selector(current_fragment, app_menu)

    # loading the CSS specific to the current page (if needed)
    special_css(current_page, get_version())

    # I can do stuff when user change page
    if is_page_changed:
        session_on_change_page()

    # navbar - automatically build from menu file
    navbar(app_menu, current_page, "app/static/images/logo.png")
    spacer(4)

    # this is where MAGIC happens - menu selects a script to run from its dictionary
    # based on the current page selected
    app_menu.get(current_page).run(
        fragment=fragment,
        static_attribute=static_attr,
        pages=app_menu.pages,
    )


if __name__ == "__main__":
    try:
        # since Streamlit's state is not saved in the browser session, I store the
        # redirect information for pages to be accessed after authentication.
        set_direct_page_link(app_menu, st.query_params)

        # learn about how I used fragment (main app's power) in its file
        current_fragment = get_fragment()

        # clean url before run
        st.query_params.clear()

        # some kind of static attribute to pass in every single page
        static_attr = 42

        # Run Barry! RUN!
        main(current_fragment, static_attr)
    except Exception as exc:
        # in this exception wrapper usually I sent exception to Sentry
        # print(exc)
        raise exc

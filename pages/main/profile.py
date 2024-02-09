from os import path

import streamlit as st
from utils.components.elements import (Attribute, ListAttribute, SubAttribute,
                                       display)
from utils.components.html import h2, spacer, title
from utils.components.page import st_user
from utils.platform.user import is_superadmin


def show(**kwargs):
    user = st_user()

    # superadmin
    if is_superadmin():
        sidesection = st.sidebar.container()
        sidesection.title("Super Section 🦸‍♂️")
        sidesection.info(
            "Hello **SUPER**! Special view only for super users (admin).",
            icon="👤",
        )

    st.title(f"Hello, {user.get('name')} 👋🏻")
    spacer(1)
    st.info(
        "Check out the **code** on _GitHub_: "
        "[MagicLit | GitHub](https://github.com/Mortafix/magiclit)",
        icon="ℹ️",
    )
    spacer(0.5)
    st.error("_Streamlit_ version: **1.31.0**", icon="🐙")
    st.divider()
    left_col, right_col = st.columns((2, 5))

    # project structure
    h2(left_col, "Project Structure", "park")
    data = {
        "script": "app.py",
        "pages": {
            "main": ["admins.py", "components.py", "heroes.py", "profile.py"],
            "general": ["developing.py"],
            "other": [],
        },
        "static": {
            "css": "all CSS files",
            "data": "static data files",
            "fonts": "all Font files",
            "images": "all Images",
        },
        "utils": {
            "components": [
                "elements.py",
                "extra.py",
                "filters.py",
                "form.py",
                "html.py",
                "navbar.py",
                "page.py",
                "selectbox.py",
                "table.py",
            ],
            "database": ["mongo.py"],
            "menu": ["app.menu", "menu.py", "parser.py"],
            "platform": ["extra.py", "user.py"],
            "web": ["fragment.py"],
        },
    }
    attributes = [
        Attribute("script"),
        SubAttribute(
            "pages",
            attributes=[
                ListAttribute("main"),
                ListAttribute("general"),
                ListAttribute("other"),
            ],
        ),
        SubAttribute(
            "static",
            attributes=[
                Attribute("css"),
                Attribute("data"),
                Attribute("images"),
            ],
        ),
        SubAttribute(
            "utils",
            attributes=[
                ListAttribute("components"),
                ListAttribute("database"),
                ListAttribute("menu"),
                ListAttribute("platform"),
                ListAttribute("web"),
            ],
        ),
    ]
    display(data, attributes, "Structure", left_col)

    # explanation
    h2(right_col, "Explanantion", "psychology_alt")
    with open(path.join(st.secrets.script.folder, "static/data/explanation.md")) as f:
        right_col.write(f.read())

    # end page space
    spacer()


def settings(**kwargs):
    title(st, 1, "Settings", "settings")
    st.info("This is where **you can change** your settings", icon="ℹ️")


def notifications(**kwargs):
    title(st, 1, "Notifications", "notifications")
    st.warning("You have **3** notifications!", icon="🔔")

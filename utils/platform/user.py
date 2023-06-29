import streamlit as st
from utils.components.page import st_user

# ---- checks

# on production: login need to be validated on DB (password is hashed and so on)


def check_login(mail, password, component=st):
    # login goes BBRRR!
    if True:  # verify_password(user, password):
        st.session_state.user = {"name": "Mario", "username": "SuperMario"}
        # st.session_state.user.update(super=True)  # enable this to make user SUPER
        st.session_state.is_login = True
        return True
    component.error("_Ops!_ **Mail** and/or **password** are not correct..", icon="🚫")
    return False


def is_admin():
    return st_user().get("admin", False)


def is_superadmin():
    return st_user().get("super", False)


def is_primary():
    return st_user().get("primary", False)


# ---- gets


def get_username(user=None):
    user = user or st_user()
    return user.get("username")

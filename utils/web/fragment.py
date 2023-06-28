from re import match, search

import streamlit as st

# Fragment is the main power of this app!
# I use the URL fragment to trigger functions in the code, since fragment is the
#   fastest way to "reload" a page

# format: URL#func-name@param1=val1&param2=val2
# example: https://app.com#download@id=42&full=auto


# simple func to split frament in function and parameters
def split_fragment(url_fragment):
    if not url_fragment or not (url_params := search(r"#(\w+)@(.+)", url_fragment)):
        return None, dict()
    function, params = url_params.groups()
    params = {
        match.group(1): match.group(2)
        for param in params.split("&")
        if (match := search(r"(\w+)=(.+)", param))
    }
    return function, params


# check if a form was submitted in st.session_state
def is_submit():
    for key in st.session_state:
        if match("FormSubmitter", key) and st.session_state.get(key):
            return True
    return False


# set a skip for next fragment
def skip_fragment():
    st.session_state["skip"] = True


# main fragment function - run the funcion!
def manage_fragment(funcs, fragment, base=False):
    if not fragment:
        return
    mode, params = split_fragment(fragment)

    # check before run - don't run if it's a refresh from st_autorefresh;
    # don't run if skip is set; don't run if a form was sumbitted
    current_refresh = st.session_state.get("main-refresh")
    is_refresh = st.session_state.get("last-refresh") != current_refresh
    is_skip = st.session_state.pop("skip", False)

    # if every condition are met and function exists in this page RUN
    if not is_skip and not is_refresh and not is_submit():
        # run the function and save the result (it can be needed later)
        if func := funcs.get(mode):
            st.session_state["last-fragment"] = fragment
            st.session_state["result"] = func(**params)
    st.session_state["last-refresh"] = current_refresh
    return mode

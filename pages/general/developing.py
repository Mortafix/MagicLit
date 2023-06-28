import streamlit as st
from utils.components.html import title


def app(**kwargs):
    title(st, 1, "Men at work", "engineering")
    st.info(
        "We are working to implement _new_ and _spectacular_ *+features**!", icon="👷‍♂️"
    )

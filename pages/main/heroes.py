import streamlit as st
from utils.components.html import title


def thor(**kwargs):
    title(st, 1, "Thor", "hardware")
    st.info(
        "_In the realm of gods and mortals, the mightiest power lies not in one's "
        "hammer, but in the courage to embrace one's destiny._",
        icon="💬",
    )


def flash(**kwargs):
    title(st, 1, "Flash", "flash_on")
    st.info(
        "_Life is a race against time, but it's not about how fast you run. It's about "
        "the moments you create and the lives you touch along the way._",
        icon="💬",
    )


def cap(**kwargs):
    title(st, 1, "Captain America", "local_police")
    st.info(
        "_A true hero isn't measured by the strength of their shield, but by the "
        "compassion in their heart._",
        icon="💬",
    )


def goku(**kwargs):
    title(st, 1, "Goku", "ramen_dining")
    st.info(
        "_Strength isn't solely found in muscles or energy blasts. It's the unyielding "
        "spirit that pushes beyond limits, always seeking greater heights._",
        icon="💬",
    )


def netero(**kwargs):
    title(st, 1, "Netero", "back_hand")
    st.info(
        "_A warrior's true strength lies not in their physical prowess, but in the "
        "wisdom gained through battles fought, and the resolve to protect what truly "
        "matters._",
        icon="💬",
    )

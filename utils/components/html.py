from base64 import b64encode
from os import path, walk
from re import sub

import streamlit as st


def _unsafe_md(markdown_text, component=st):
    component.markdown(markdown_text, unsafe_allow_html=True)


# ---- CSS


@st.cache_data(persist=True, show_spinner=False)
def multiple_local_css(version):
    css_order = {"smartphone.css": 2, "video.css": -1}
    css_contents = str()
    css_files = list(walk(path.join(st.secrets.script.folder, "static/css")))[0][2]
    for file in sorted(css_files, key=lambda file: css_order.get(file, 0)):
        if file.endswith(".css"):
            with open(path.join(st.secrets.script.folder, "static/css", file)) as f:
                css_contents += f.read()
    _unsafe_md(f"<style>{css_contents}</style>")


@st.cache_data(persist=True, show_spinner=False)
def remote_css(url):
    _unsafe_md(f"<link href='{url}' rel='stylesheet'>")


@st.cache_data(persist=True, show_spinner=False)
def special_css(page, version):
    special = {
        "hero-thor": ["thor.css"],
        "hero-flash": ["flash.css"],
        "hero-cap": ["cap.css"],
        "hero-goku": ["goku.css"],
        "hero-netero": ["netero.css"],
    }
    css_contents = str()
    for file in special.get(page, []):
        with open(path.join(st.secrets.script.folder, "static/css/special", file)) as f:
            css_contents += f.read()
    _unsafe_md(f"<style>{css_contents}</style>")


@st.cache_data(persist=True, show_spinner=False)
def login_css(version):
    with open(path.join(st.secrets.script.folder, "static/css/special/login.css")) as f:
        css_contents = f.read()
    _unsafe_md(f"<style>{css_contents}</style>")


@st.cache_data(persist=True, show_spinner=False)
def remove_streamlit_menu():
    _unsafe_md("<style>#MainMenu, footer, header {visibility: hidden;}</style>")


# ---- HTML


@st.cache_data(persist=True, show_spinner=False)
def icon(icon_name, size=24, other_class=""):
    return (
        f"<i class='material-icons {other_class}' style='font-size:{size}px'>"
        f"{icon_name}</i>"
    )


def spacer(height=1, component=st):
    _unsafe_md(f"<div style='height:{1 * height + 1}rem'></div>", component)


def div(component, _class="", text="", style="", **kwargs):
    attributes = " ".join(f"{attr}='{value}'" for attr, value in kwargs.items())
    _unsafe_md(f"<div class='{_class}' {attributes} {style}>{text}</div>", component)


def image(img_url, _class, component=st):
    return div(component, _class, f"<img src='{img_url}'>")


def svg(svg_file, _class, component=st):
    with open(path.join(st.secrets.script.folder, "static/images/", svg_file)) as file:
        return div(component, _class, file.read())


def iframe(src, component=st, **params):
    iframe_params = " ".join(f"{attr}={val}" for attr, val in params.items())
    _unsafe_md(f"<iframe src='{src}' {iframe_params}></iframe>", component)


# ---- titles


def title(component, dimension, text, icon_name):
    _unsafe_md(f"<h{dimension}>{icon(icon_name)}{text}</h{dimension}>", component)


def h2(component, text, icon_name):
    title(component, 2, text, icon_name)


def h4(component, text, icon_name):
    title(component, 4, text, icon_name)


# ---- buttons


def redirect_button(text, over_icon=None, url=None, component=st):
    if not url and not (page := st.session_state.get("redirect-page")):
        return
    url = url or page.url
    icon_name = over_icon or page.icon
    html_btn = f"<a href='#url@page={url}'>{icon(icon_name)}<span>{text}</span></a>"
    div(component, "redirect-btn mirror", html_btn)


#  ---- files


def show_file(file, file_fmt=None, width=400, height=570, style=None, component=st):
    base64_pdf = b64encode(file).decode("utf-8")
    style_html = ";".join(f"{attr}:{value}" for attr, value in style.items() or dict())
    pdf_display = (
        f"<iframe src='data:{file_fmt};base64,{base64_pdf}' width='{width}' "
        f"height='{height}' style='{style_html}' type='{file_fmt}'></iframe>"
    )
    _unsafe_md(pdf_display, component=component)


def show_a4_pdf(file, file_format, vertical=True, size=100, component=st):
    style = {"aspect-ratio": "1 / 1.43" if vertical else "1.43 / 1"}
    show_file(file, file_format, f"{size}%", "auto", style=style, component=component)


def pdf_preview_download(
    file, file_format, filename, data=True, vertical=True, columns=(2, 3)
):
    col_pdf, col_btn = st.columns(columns)
    col_btn.download_button(
        label="Download **PDF** 📝",
        data=file if data else file.read(),
        file_name=f"{filename}.{file_format.split('/')[-1]}",
        mime=file_format,
    )
    col_btn.button("Chiudi ❌")
    file.seek(0)
    show_a4_pdf(file.read(), file_format, vertical, component=col_pdf)


# ---- web notifications


class Notification:
    def __init__(self, text, icon_name="", other_class="", color_bg="", color_text=""):
        self.icon_name = icon_name or "thumb_up"
        self.text = self.md_parsing(text)
        self.style = ""
        self._class = other_class

    def md_parsing(self, text):
        text = sub(r"[\*\_]{2}(.+?)[\*\_]{2}", r"<b>\g<1></b>", text)
        text = sub(r"[\*\_](.+?)[\*\_]", r"<i>\g<1></i>", text)
        return text

    # notifications type

    def success(self, icon_name="check_circle"):
        self._class = "noti-success"
        self.icon_name = icon_name
        self._show()

    def info(self, icon_name="info"):
        self._class = "noti-info"
        self.icon_name = icon_name
        self._show()

    def warning(self, icon_name="warning"):
        self._class = "noti-warning"
        self.icon_name = icon_name
        self._show()

    def error(self, icon_name="dangerous"):
        self._class = "noti-error"
        self.icon_name = icon_name
        self._show()

    def custom(self, icon_name, color_bg):
        self.style = f"style='background-color: {color_bg}'"
        self.icon_name = icon_name
        self._show()

    def _show(self):
        html_notification = (
            f"<a href='#'><span>{icon(self.icon_name)}{self.text}</span></a>"
        )
        if prev_noti := st.session_state.pop("custom-notification", None):
            prev_noti.empty()
        self.noti_object = div(
            st, f"notification {self._class}", html_notification, self.style
        )
        st.session_state.notification = self.noti_object

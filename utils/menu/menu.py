from pages.main import admins, components, heroes, profile
from utils.menu.parser import parse_menu

main_pages = {
    "component-element": components.element,
    "component-form": components.form,
    "component-title": components.titles,
    "component-notification": components.notification,
    "component-selectbox": components.selectbox,
    "component-table": components.tables,
    "component-extra": components.extra,
    "hero-thor": heroes.thor,
    "hero-flash": heroes.flash,
    "hero-cap": heroes.cap,
    "hero-goku": heroes.goku,
    "hero-netero": heroes.netero,
    "admins-list": admins.show,
    "profile": profile.show,
    "profile-settings": profile.settings,
    "profile-notifications": profile.notifications,
}

app_menu = parse_menu("app", main_pages)

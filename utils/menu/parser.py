from re import sub

from pages.general import developing

# ---- Classes


class Menu(dict):
    def __init__(self, main_pages):
        self.pages = main_pages
        self.free_pages = list()
        pages_redirect = {page.url: page for page in main_pages if page.url}
        subpages_redirect = {
            page.url: page for subpages in main_pages for page in subpages.pages
        }
        subred_redirect = {
            page.redirect.url: page.redirect
            for subpages in main_pages
            for page in subpages.pages
            if page.redirect
        }
        self.update({**pages_redirect, **subpages_redirect, **subred_redirect})

    def first_page(self, page):
        self.first = page

    def add_free_pages(self, pages):
        self.free_pages = pages
        free_pages_entries = {page.url: page for page in pages}
        free_rediret_entries = {
            page.redirect.url: page.redirect for page in pages if page.redirect
        }
        pages_to_add = {**free_pages_entries, **free_rediret_entries}
        self.update(**pages_to_add)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        return f"Menu {dict.__repr__(self)}"

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class TemplatePage:
    def __init__(self, title, icon, url, function, dev, hidden, first, sadmin, active):
        self.title = title
        self.icon = icon
        self.url = url
        self.function = function
        self.developing = dev
        self.hidden = hidden
        self.is_first = first
        self.super_admin = sadmin
        self.main = active
        self.redirect = None
        self.pages = list()
        self.free_pages = list()

    def __repr__(self):
        return f"{self.title}:{self.icon}"

    def run(self, **kwargs):
        if self.function:
            self.function(**kwargs)


class MainPage(TemplatePage):
    def add_subpage(self, page):
        self.pages.append(page)

    def add_freepage(self, page):
        self.free_pages.append(page)

    def __repr__(self):
        return super().__repr__() + f" [{', '.join(map(str, self.pages))}]"

    def contains(self, other_url):
        if self.url == other_url:
            return True
        return any(
            page.url == other_url or (page.redirect and page.redirect.url == other_url)
            for page in self.pages + self.free_pages
        )


class SubPage(TemplatePage):
    def add_redirect(self, redirect):
        self.redirect = redirect
        self.redirect.redirect = self


class FreePage(TemplatePage):
    def add_function(self, function):
        self.function = function

    def add_redirect(self, redirect):
        self.redirect = redirect
        self.redirect.redirect = self


class Redirect(TemplatePage):
    ...


# ---- Parser


def get_page(pages, url, is_dev, is_hidden):
    if is_dev or is_hidden:
        return developing.app
    return pages.get(url)


def get_main_attribute(attributes):
    chars = [token for token in attributes if token in ":@#"]
    attributes = sub(r"[:@#]", ",", " ".join(attributes)).split(",")
    title, *attributes = attributes
    icon, url, active = None, None, None
    for delimiter, attribute in zip(chars, attributes):
        if delimiter == ":":
            icon = attribute.strip()
        if delimiter == "@":
            url = attribute.strip()
        if delimiter == "#":
            active = attribute.strip()
    return title.strip(), icon, url, active


def get_dev_options(page_type):
    is_superadmin = "!" in page_type
    is_dev = "?" in page_type
    is_hidden = "/" in page_type
    first_page = "1" in page_type
    return is_superadmin, is_dev, is_hidden, first_page


def line_parser(line, page_scripts):
    page, *attributes = line.split(" ")
    sadmin, is_dev, is_hidden, first = get_dev_options(page)
    title, icon, url, active = get_main_attribute(attributes)
    if not (func := get_page(page_scripts, url, is_dev, is_hidden)) and url:
        raise ValueError(f"Missing '{title} ({url})' function")
    page_types = {"*": MainPage, ">": Redirect, "-": SubPage, "+": FreePage}
    return page_types.get(page[0])(
        title, icon, url, func, is_dev, is_hidden, first, sadmin, active
    )


def parse_menu(subdomain, page_scripts):
    file = open(f"utils/menu/{subdomain}.menu").read()
    lines = [line.strip() for line in file.split("\n") if line]
    menu_pages, first_page, free_pages = list(), None, list()
    free_page_zone, last_idx_free = False, None
    for line in lines:
        page = line_parser(line, page_scripts)
        if isinstance(page, MainPage):
            menu_pages.append(page)
        if isinstance(page, SubPage):
            menu_pages[-1].add_subpage(page)
        if isinstance(page, Redirect):
            if free_page_zone:
                if last_idx_free is None:
                    free_pages[-1].add_redirect(page)
                else:
                    menu_pages[last_idx_free].free_pages[-1].add_redirect(page)
            else:
                menu_pages[-1].pages[-1].add_redirect(page)
        if isinstance(page, FreePage):
            free_page_zone = True
            free_pages.append(page)
            for i in range(len(menu_pages)):
                if page.main == menu_pages[i].title:
                    last_idx_free = i
                    menu_pages[i].add_freepage(page)
                    break
        if page.is_first:
            first_page = page
    menu = Menu(menu_pages)
    menu.add_free_pages(free_pages)

    # first page
    if not first_page:
        raise Exception("First page missing!")
    menu.first_page(first_page)
    # final check
    for page in page_scripts:
        if not menu.get(page):
            raise Exception(f"No page found for '{page}' url")
    return menu

import streamlit as st
from utils.components.html import div


class IAttribute:
    def _dot_attribute(self, data):
        if self.attribute and "." in self.attribute:
            for attr in self.attribute.split(".")[:-1]:
                data = data.get(attr)
            self.attribute = self.attribute.split(".")[-1]
        return data

    def _div(self, label, data):
        if not data:
            return ""
        return f"<div class='attribute-row'><span>{label.title()}</span>{data}</div>"


class Attribute(IAttribute):
    def __init__(self, attribute=None, label=None, func=None):
        self.attribute = attribute
        self.label = label or attribute
        self.func = func or (lambda x: x)

    def html(self, data, index=None):
        if not (data := self._dot_attribute(data)):
            return ""
        final_data = self.func(data.get(self.attribute) if self.attribute else data)
        if index is not None:
            self.label = str(index)
        return self._div(self.label, final_data)


class CombinedAttribute(IAttribute):
    def __init__(self, attributes, label, func=None):
        self.attributes = attributes
        self.label = label or " ".join(attributes)
        self.func = func or (lambda x: " ".join(str(el) for el in x))

    def html(self, data):
        if not data:
            return ""
        final_data = self.func([data.get(attr) for attr in self.attributes])
        return self._div(self.label, final_data)


class SubAttribute(IAttribute):
    def __init__(self, attribute=None, label=None, attributes=None):
        self.attribute = attribute
        self.label = label or attribute
        self.attributes = attributes or list()

    def html(self, data, index=None):
        data = self._dot_attribute(data)
        elem = data.get(self.attribute) if self.attribute else data
        final_data = "".join(attribute.html(elem) for attribute in self.attributes)
        if index is not None:
            self.label = str(index)
        return self._div(self.label, f"<div class='sub'>{final_data}</div>")


class ListAttribute(IAttribute):
    def __init__(self, attribute, label=None, single=None):
        self.attribute = attribute
        self.label = label or attribute
        self.single = single or Attribute()

    def html(self, data):
        if not (data := self._dot_attribute(data)):
            return ""
        final_data = "".join(
            self.single.html(entry, index=i)
            for i, entry in enumerate(data.get(self.attribute, []), 1)
        )
        return self._div(self.label, f"<div class='sub'>{final_data}</div>")


def display(data, attributes, title=None, component=st):
    text = "".join(attribute.html(data) for attribute in attributes)
    html = f"<div class='title'>{title}</div>{text}" if title else text
    return div(component, _class="attributes", text=html)

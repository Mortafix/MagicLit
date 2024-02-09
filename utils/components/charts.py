import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ---- utils


def lighten_color(hex_color, amount=0.25):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def text_shorten(text, max_chars=15):
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_chars else text[:max_chars] + ".."


# ---- component


class Chart:
    fig = None

    def __init__(self, data, component=st):
        self.X = list(data)
        self.Y = list(data.values())
        self.Xt = np.arange(len(data))
        if not self.Y:
            self.n_bars = 1
            return
        # transpose
        if not isinstance(self.Y[0], list):
            self.Y = [[val] for val in self.Y]
        self.Y = [
            [self.Y[i][j] for i in range(len(self.Y))] for j in range(len(self.Y[0]))
        ]
        self.n_bars = len(self.Y)
        self.component = component
        self.options()

    def options(
        self,
        size=None,
        show_grid=False,
        show_ticks=True,
        color="#588157",
        labels=None,
        label_max_chars=15,
    ):
        self.size = size or (6, 4)
        self.colors = [color] if not isinstance(color, list) else color
        self.colors = self.colors + self.colors * self.n_bars
        self.labels = labels or list(range(len(self.Y)))
        self.grid = show_grid
        self.ticks = show_ticks
        self.label_max = label_max_chars

    # chart types

    def bar(self, bar_width=0.7, horizontal=False):
        self.graph_type = "bar" if not horizontal else "barh"
        self.bar_tot_width = bar_width
        self.bar_width = self.bar_tot_width / self.n_bars

    def plot(self, line_width=1, marker="", marker_size=7):
        self.graph_type = "plot"
        self.area = False
        self.marker = marker
        self.marker_size = marker_size
        self.line_width = line_width

    def area(self):
        self.graph_type = "plot"
        self.area = True
        self.marker = ""
        self.marker_size = 0
        self.line_width = 1.5

    def donut(self, size):
        self.graph_type = "donut"
        self.donut_size = size

    # show chart

    def show(self, title=None, subtitle=None, xlabel="", ylabel="", legend=False):
        if not self.Y:
            return
        fig, ax = plt.subplots(figsize=self.size)
        self.fig = fig
        # ---- data
        # bar
        if self.graph_type in ("bar", "barh"):
            for i, (y_vals, color) in enumerate(zip(self.Y, self.colors)):
                (ax.bar if self.graph_type == "bar" else ax.barh)(
                    self.Xt
                    - self.bar_tot_width / 2
                    + (self.bar_width * i)
                    + (self.bar_width / 2),
                    y_vals,
                    self.bar_width,
                    color=color,
                    label=self.labels[i],
                )
        # plot | area
        if self.graph_type in ("plot", "area"):
            for i, (y_vals, color) in enumerate(zip(self.Y, self.colors)):
                ax.plot(
                    self.Xt,
                    y_vals,
                    linewidth=self.line_width,
                    marker=self.marker,
                    markersize=self.marker_size,
                    color=color,
                    label=self.labels[i],
                )
                if self.area:
                    ax.fill_between(self.Xt, y_vals, color=color)
        # donut
        if self.graph_type == "donut":
            predata = {label: value for label, value in zip(self.X, self.Y[0]) if value}
            labels = list(predata)[:10]
            data = list(predata.values())[:10]
            wedges, _ = ax.pie(
                data,
                startangle=90,
                counterclock=False,
                colors=[
                    lighten_color(self.colors[0], i * 1 / len(data))
                    for i in range(len(data))
                ],
            )
            plt.setp(wedges, width=self.donut_size, edgecolor="white")
            kw = {
                "arrowprops": {"arrowstyle": "-"},
                "bbox": dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72),
                "zorder": 0,
                "va": "center",
            }
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                if not legend:
                    ax.annotate(
                        text_shorten(labels[i], 30),
                        xy=(x, y),
                        xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment,
                        **kw,
                    )
            if legend:
                ax.legend(
                    wedges,
                    [text_shorten(x, 30) for x in labels],
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1),
                )

        # style
        ax.set_facecolor((1, 1, 1, 0.1))
        fig.patch.set_alpha(0.1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if self.grid:
            ax.grid(linewidth=0.2)
        # ticks
        if self.graph_type != "donut":
            is_horiz = self.graph_type == "barh"
            ax.set_xticks(self.Xt) if not is_horiz else ax.set_yticks(self.Xt)
            label_tick_f = ax.set_xticklabels if not is_horiz else ax.set_yticklabels
            must_rotate = max(len(str(t)) for t in self.X) > 10 or len(self.X) > 15
            rotation = 90 if not is_horiz and must_rotate else 0
            label_tick_f(
                [text_shorten(x, self.label_max) for x in self.X], rotation=rotation
            )
            if not self.ticks:
                plt.tick_params(
                    left=False,
                    right=False,
                    labelleft=False,
                    labelbottom=False,
                    bottom=False,
                )
        # labels
        if xlabel and self.graph_type != "donut":
            ax.set_xlabel(xlabel)
        if ylabel and self.graph_type != "donut":
            ax.set_ylabel(ylabel)
        if title:
            plt.suptitle(title, fontsize=20, y=1)
        if subtitle:
            plt.title(subtitle, fontsize=14)
        if legend and len(self.Y) > 1:
            plt.legend(loc="upper right")
        # output
        self.component.pyplot(self.fig, use_container_width=False)

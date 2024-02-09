import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---- utils


def calculate_center(latitude, longitude):
    return {
        "lat": sum(latitude) / len(latitude),
        "lon": sum(longitude) / len(longitude),
    }


def calculate_zoom(latitude, longitude, amount=12):
    lat_range = max(latitude) - min(latitude)
    lon_range = max(longitude) - min(longitude)
    max_bound = max(lat_range, lon_range, 0.5) * 111
    return amount - np.log(max_bound)


# ---- map


def geomap(points, height=1000, base_color="#4ba2ff", component=st):
    lat_points, lon_points = [p[1] for p in points], [p[2] for p in points]
    colors = [p[3] if len(p) == 4 else base_color for p in points]
    fig = go.Figure(
        go.Scattermapbox(
            lat=lat_points,
            lon=lon_points,
            text=[p[0] for p in points],
            hoverinfo="text",
            marker={"size": 12, "color": colors},
        )
    )
    fig.update_layout(
        margin={"t": 0, "b": 0},
        mapbox={
            "style": "carto-positron",
            "center": calculate_center(lat_points, lon_points),
            "zoom": calculate_zoom(lat_points, lon_points),
            "layers": [{"maxzoom": 1}],
        },
        height=height,
        hoverlabel={
            "bgcolor": base_color,
            "font": {"color": "#FFF", "size": 20, "family": "source sans pro"},
        },
    )
    map_config = {"displayModeBar": False, "scrollZoom": True}
    return component.plotly_chart(fig, config=map_config, use_container_width=True)

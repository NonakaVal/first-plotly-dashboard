import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


# =========================
# Load data
# =========================

df = pd.read_csv("GlobalWeatherRepository.csv")

df["last_updated"] = pd.to_datetime(df["last_updated"])


# =========================
# Create Dash app
# =========================

app = dash.Dash(__name__)


# =========================
# Average temperature by location
# =========================

average_temperature = (
    df.groupby(
        ["latitude", "longitude", "location_name"]
    )
    .agg({
        "temperature_celsius": "mean"
    })
    .reset_index()
)

average_temperature["temperature_celsius"] = (
    average_temperature["temperature_celsius"].round(2)
)


# =========================
# Temperature map
# =========================

map_plot = px.scatter_map(
    average_temperature,
    lat="latitude",
    lon="longitude",
    hover_name="location_name",
    color="temperature_celsius",
    title="Average Temperature Map"
)

map_plot.update_layout(
    map_style="open-street-map",
    height=800,
    width=900,
    font=dict(size=18),
    map=dict(
        center=dict(
            lat=0,
            lon=0
        ),
        zoom=1
    ),
    coloraxis=dict(
        colorbar=dict(
            title="°C"
        )
    )
)


# =========================
# Box plot
# =========================

box_chart = px.box(
    df,
    x="country",
    y="temperature_celsius",
    title="Average Temperature by Country"
)

box_chart.update_layout(
    height=1000,
    width=2050,
    font=dict(size=18)
)


# =========================
# Temperature trends
# =========================

line_plot = px.line(
    df,
    x="last_updated",
    y="temperature_celsius",
    title="Temperature Trends (double-click in country)",
    color="country",
    markers=True,
    text="humidity"
)

line_plot.update_traces(
    textposition="top center",
    textfont=dict(size=15)
)

line_plot.update_layout(
    legend_title_text="Country",
    height=800,
    width=1800,
    font=dict(size=18)
)

line_plot.update_traces(
    line=dict(width=3),
    marker=dict(
        size=12,
        line=dict(
            width=1,
            color="DarkSlateGrey"
        )
    )
)


# =========================
# Dashboard layout
# =========================

app.layout = html.Div([

    html.H1(
        "Exploratory analysis of climate data",
        style={
            "text-align": "center",
            "font-family": "Arial, sans-serif",
            "font-size": "2em",
            "margin-top": "50px"
        }
    ),

    # Line chart + Map
    html.Div(
        [

            dcc.Graph(
                figure=line_plot,
                id="line-plot",
                style={
                    "width": "50%",
                    "flex": 1
                }
            ),

            dcc.Graph(
                figure=map_plot,
                id="map-plot",
                style={
                    "width": "50%",
                    "flex": 1,
                    "marginRight": "30px"
                }
            )

        ],
        style={
            "width": "130%",
            "display": "flex",
            "justify-content": "space-between",
            "margin": "auto"
        }
    ),

    # Box chart
    html.Div(
        [

            dcc.Graph(
                figure=box_chart,
                id="box-chart",
                style={
                    "width": "100%",
                    "flex": 1,
                    "margin-top": "20px"
                }
            )

        ],
        style={
            "width": "100%",
            "display": "flex",
            "justify-content": "center"
        }
    )

])


# =========================
# Run application
# =========================

if __name__ == "__main__":
    app.run(debug=True)

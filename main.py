import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

df = pd.read_csv('GlobalWeatherRepository.csv')
df['last_updated'] = pd.to_datetime(df['last_updated'])

app = dash.Dash(__name__)

average_temperature = df.groupby(['latitude', 'longitude', 'location_name']).agg({'temperature_celsius': 'mean'}).reset_index()
average_temperature['temperature_celsius'] = round(average_temperature['temperature_celsius'], 2)  # Arredonde para 2 casas decimais

mapbox_plot = px.scatter_mapbox(average_temperature, lat='latitude', lon='longitude', hover_name='location_name',
                                color='temperature_celsius', title='Average Temperature Map')
mapbox_plot.update_layout(mapbox_style='open-street-map', height=800, width=900, font=dict(size=18),
                          mapbox=dict(center=dict(lat=0, lon=0), zoom=1))
mapbox_plot.update_layout(coloraxis=dict(colorbar=dict(title='°C')))


box_chart = px.box(df, x='country', y='temperature_celsius', title='Average Temperature by Country')

box_chart.update_layout(height=1000, width=2050, font=dict(size=18))


line_plot = px.line(df, x='last_updated', y='temperature_celsius', title="Temperature Trends (double-click in country)",
                    color="country", markers=True, text="humidity")

line_plot.update_traces(textposition='top center', textfont=dict(size=15))
line_plot.update_layout(legend_title_text='Country', height=800, width=1800,font=dict(size=18))
line_plot.update_traces(line=dict(width=3), marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))


app.layout = html.Div([

    html.H1("Exploratory analysis of climate data", style={'text-align': 'center', 'font-family': 'Arial, sans-serif', 'font-size': '2em', 'margin-top': '50px'}),

    html.Div([
        dcc.Graph(figure=line_plot, id='line-plot', style={'width': '50%', 'flex': 1}),

        dcc.Graph(figure=mapbox_plot, id='mapbox-plot', style={'width': '50%', 'flex': 1, 'marginRight': '30px'}),
    ], style={'width': '130%', 'display': 'flex', 'justify-content': 'space-between', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(figure=box_chart, id='box-chart', style={'width': '100%', 'flex': 1, 'margin-top': '20px'}),
    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}),
])



if __name__ == '__main__':
    app.run_server(debug=True)








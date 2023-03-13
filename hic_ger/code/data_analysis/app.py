import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import json


providers_path = "../../data/providers_cleaned.csv"
states_path = "../../data/states_cleaned.csv"
states_map_path = "../../data/german_states.geo.json"
df_prov = pd.read_csv(providers_path)
df_states = pd.read_csv(states_path)

# Create bar plots
fig = px.bar(df_prov, 'fee', 'name')
bar_plot_fees = dcc.Graph(id='bar plot fees', figure=fig)
fig = px.bar(df_prov, 'services_count', 'name')
bar_plot_services = dcc.Graph(id='bar plot services', figure=fig)
fig = px.bar(df_states,'provider_count', 'Unnamed: 0')
bar_plot_states = dcc.Graph(id='bar plot states', figure=fig)

#Create maps
with open(states_map_path) as f:
    geojson_states = json.load(f)

fig_fees = px.choropleth_mapbox(df_states,
                           geojson=geojson_states,
                           color='avg_fee',
                           featureidkey='properties.name',
                           locations='Unnamed: 0',
                           center={"lat": 51.1656, "lon": 10.4515},
                           zoom=4,
                           mapbox_style="white-bg"
                           )
fig_services = px.choropleth_mapbox(df_states,
                           geojson=geojson_states,
                           color='avg_services_count',
                           featureidkey='properties.name',
                           locations='Unnamed: 0',
                           center={"lat": 51.1656, "lon": 10.4515},
                           zoom=4,
                           mapbox_style="white-bg"
                           )
fig_providers = px.choropleth_mapbox(df_states,
                           geojson=geojson_states,
                           color='provider_count',
                           featureidkey='properties.name',
                           locations='Unnamed: 0',
                           center={"lat": 51.1656, "lon": 10.4515},
                           zoom=4,
                           mapbox_style="white-bg"
                           )

map_plot_fees = dcc.Graph(id='map plot fees', figure=fig_fees)
map_plot_services = dcc.Graph(id='map plot services', figure=fig_services)
map_plot_providers = dcc.Graph(id='map plot providers', figure=fig_providers)




# Initialise the app
app = Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.H2('Health Insurance Comparison', className='row'),
    html.Div('Text Information', className='row'),
    html.Div(className='column', children=[
        html.Div(bar_plot_fees),
        html.Div(bar_plot_services),
        html.Div(bar_plot_states)
    ]),
    html.Div(className='column', children=[
        html.Div(map_plot_fees),
        html.Div(map_plot_services),
        html.Div(map_plot_providers)
    ]),
    html.Div('Graph area 3', className='column')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
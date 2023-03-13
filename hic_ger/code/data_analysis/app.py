import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import json

providers_path = "../../data/providers_cleaned.csv"
states_path = "../../data/states_cleaned.csv"
states_map_path = "../../data/german_states.geo.json"
df_prov = pd.read_csv(providers_path, index_col=0)
df_states = pd.read_csv(states_path, index_col=0)

#Create box plots
fig_fee = px.box(df_prov, y='fee')
fig_services = px.box(df_prov, y='services_count')
fig_avgfees = px.box(df_states, y='avg_fee')
fig_avgservices = px.box(df_states, y='avg_services_count')
fig_provider = px.box(df_states, y='provider_count')

box_plot_fees = dcc.Graph(id='box plot fees', figure=fig_fee)
box_plot_services = dcc.Graph(id='box plot services', figure=fig_services)
box_plot_avgfees = dcc.Graph(id='box plot avgfees', figure=fig_avgfees)
box_plot_avgservices = dcc.Graph(id='box plot avgservices', figure=fig_avgservices)
box_plot_provider = dcc.Graph(id='box plot provider', figure=fig_provider)

# Create bar plots
fig = px.bar(df_prov.sort_values('fee'), 'fee', 'name',
             title='Additional Fees charged by each Provider',
             labels={'fee': 'Additional Fees (%)'})
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(title_text='')
bar_plot_fees = dcc.Graph(id='bar plot fees', figure=fig)
fig = px.bar(df_prov.sort_values('services_count'), 'services_count', 'name',
             title='Number of Services offered by each Provider',
             labels={'services_count':'Number of Services offered'})
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(title_text='')
bar_plot_services = dcc.Graph(id='bar plot services', figure=fig)
fig = px.bar(df_states.sort_values('provider_count'), 'provider_count', 'state',
             title='Number of Providers per State',
             labels={'provider_count': 'Number of Providers'})
fig.update_yaxes(title_text='')
bar_plot_states = dcc.Graph(id='bar plot states', figure=fig)

# Create maps
with open(states_map_path) as f:
    geojson_states = json.load(f)

fig_fees = px.choropleth_mapbox(df_states,
                                geojson=geojson_states,
                                color='avg_fee',
                                featureidkey='properties.name',
                                locations='state',
                                center={"lat": 51.1656, "lon": 10.4515},
                                zoom=4,
                                mapbox_style="white-bg",
                                labels={'avg_fee': 'average fee(%)'},
                                title='Average Fees per State',
                                color_continuous_scale='blues',
                                range_color=[1.4,1.5]
                                )
fig_services = px.choropleth_mapbox(df_states,
                                    geojson=geojson_states,
                                    color='avg_services_count',
                                    featureidkey='properties.name',
                                    locations='state',
                                    center={"lat": 51.1656, "lon": 10.4515},
                                    zoom=4,
                                    mapbox_style="white-bg",
                                    labels={'avg_services_count': 'average number of services'},
                                    title='Average Number of Services per State',
                                    color_continuous_scale='blues',
                                    range_color=[95,105]
                                    )
fig_providers = px.choropleth_mapbox(df_states,
                                     geojson=geojson_states,
                                     color='provider_count',
                                     featureidkey='properties.name',
                                     locations='state',
                                     center={"lat": 51.1656, "lon": 10.4515},
                                     zoom=4,
                                     mapbox_style="white-bg",
                                     labels={'provider_count': 'number of providers'},
                                     title='Number of Providers per State',
                                     color_continuous_scale='blues',
                                     range_color=[35,45]
                                     )



map_plot_fees = dcc.Graph(id='map plot fees', figure=fig_fees)
map_plot_services = dcc.Graph(id='map plot services', figure=fig_services)
map_plot_providers = dcc.Graph(id='map plot providers', figure=fig_providers)

#Create scatter plots
fig_prov = px.scatter(df_prov, x='fee', y='services_count',
                      labels={'fee':'Additional Fees (%)', 'services_count': 'Number of Services offered'},
                      hover_name='name',
                      title='Correlation between Fees and Number of Services offered by providers')
fig_states = px.scatter(df_states, x='avg_fee', y='avg_services_count',
                        labels={'avg_fee':'Average Fees (%)', 'avg_services_count': 'Average Number of Services Offered'},
                        hover_name='state',
                        title='Correlation between Average Fee and Average Number of Services Offered in German States')
scatter_plot_prov = dcc.Graph(id='scatter plot prov', figure=fig_prov)
scatter_plot_states = dcc.Graph(id='scatter plot states', figure=fig_states)

# Initialise the app
app = Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.H2('Health Insurance Comparison', className='row'),
    html.Div(className='row', children=[
        html.Div(box_plot_fees, className='column'),
        html.Div(box_plot_services, className='column'),
        html.Div(box_plot_avgfees, className='column'),
        html.Div(box_plot_avgservices, className='column'),
        html.Div(box_plot_provider, className='column')
    ]),
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
    html.Div(className='column', children=[
        html.Div(scatter_plot_prov),
        html.Div(scatter_plot_states)
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import json

providers_path = "../../data/providers_cleaned.csv"
states_path = "../../data/states_cleaned.csv"
states_map_path = "../../data/german_states.geo.json"
df_prov = pd.read_csv(providers_path, index_col=0)
df_states = pd.read_csv(states_path, index_col=0)

# Create bar plots
fig = px.bar(df_prov.sort_values('fee'), 'fee', 'name',
             title='Fees charged by each Provider',
             labels={'fee': 'Fees (%)'})
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(title_text='')
bar_plot_fees = dcc.Graph(id='bar plot fees', figure=fig)
fig = px.bar(df_prov.sort_values('services_count'), 'services_count', 'name',
             title='Number of Services offered by each Provider',
             labels={'services_count': 'Number of Services offered'})
fig.update_yaxes(showticklabels=False)
fig.update_yaxes(title_text='')
bar_plot_services = dcc.Graph(id='bar plot services', figure=fig)
fig = px.bar(df_states.sort_values('provider_count'), 'provider_count', 'state',
             title='Number of Providers by State',
             labels={'provider_count': 'Number of Providers'})
fig.update_yaxes(title_text='')
bar_plot_states = dcc.Graph(id='bar plot states', figure=fig)
fig = px.bar(df_states.sort_values('avg_fee'), 'avg_fee', 'state',
             title='Average Fee by State',
             labels={'avg_fee': 'Average Fee'})
fig.update_yaxes(title_text='')
bar_plot_avgfees = dcc.Graph(id='bar plot avgfees', figure=fig)
fig = px.bar(df_states.sort_values('avg_services_count'), 'avg_services_count', 'state',
             title='Average Number of Services by State',
             labels={'avg_services_count': 'Average number of services'})
fig.update_yaxes(title_text='')
bar_plot_avgservices = dcc.Graph(id='bar plot avgservices', figure=fig)

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
                                title='Average Fee by State',
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
                                    title='Average Number of Services by State',
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
                                     title='Number of Providers by State',
                                     color_continuous_scale='blues',
                                     range_color=[35,45]
                                     )



map_plot_fees = dcc.Graph(id='map plot fees', figure=fig_fees)
map_plot_services = dcc.Graph(id='map plot services', figure=fig_services)
map_plot_providers = dcc.Graph(id='map plot providers', figure=fig_providers)

#Create scatter plots
fig_prov = px.scatter(df_prov, x='fee', y='services_count',
                      labels={'fee': 'Fees (%)', 'services_count': 'Number of Services offered'},
                      hover_name='name',
                      title='Correlation between Fees and Number of Services offered by Providers')
fig_states = px.scatter(df_states, x='avg_fee', y='avg_services_count',
                        labels={'avg_fee':'Average Fees (%)', 'avg_services_count': 'Average Number of Services Offered'},
                        hover_name='state',
                        title='Correlation between Average Fee and Average Number of Services Offered')
scatter_plot_prov = dcc.Graph(id='scatter plot prov', figure=fig_prov)
scatter_plot_states = dcc.Graph(id='scatter plot states', figure=fig_states)

# Initialise the app
app = Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.H2('Statutory Health Insurance Companies in Germany', className='row'),
    html.H3('Introduction', className='row'),
    html.Div(
        [
            'This dashboard gives an overview about the fees charged by german statutory health insurance companies, '
            'as well as the number of services offered by them. The first part of the visualisations gives information '
            'on the individual companies (in the following called providers for reasons of brevity), whereas the '
            'second part accumulates the data on state level. The data on fees comes from the ',
            dcc.Link('german central association on statutory health insurance providers',
                  href='https://www.gkv-spitzenverband.de/service/krankenkassenliste/krankenkassen.jsp'),
            '. Statutory health insurance fees in Germany are determined by a fixed percentage of 14.6% of the '
            'customer\'s income. This base fee is independent of the provider. On top of that, each provider '
            'charges an additional fee that that is also determined by a percentage of the customer\'s income. These '
            'additional fees are the ones depicted in the visualizations below. The data on the number of services '
            'offered comes from the website ',
            dcc.Link('https://www.krankenkassen.de/', href='https://www.krankenkassen.de/'),
            ', which is a comparison portal for health insurance providers. It is not an official source and the way '
            'they collect their data is not known. Furthermore, not all german providers are included in their '
            'comparison. The services they track are financial support for medical services like cancer screening, '
            'but also administrative services like providing apps, hotlines and consultation. Without validating the '
            'data collection process and the categorization of services from this source, the insights taken from this '
            'dataset should be regarded as uncertain. '
        ],
        className='row'
    ),
    html.H3('Data Grouped by Providers', className='row'),
    html.Div(bar_plot_fees, className='column'),
    html.Div(bar_plot_services, className='column'),
    html.Div(scatter_plot_prov, className='column'),
    html.H3('Data Grouped by States', className='row'),
    html.Div(className='row', children=[
        html.Div(bar_plot_avgfees, className='column'),
        html.Div(bar_plot_avgservices, className='column'),
        html.Div(bar_plot_states, className='column')
    ]),
    html.Div(className='row', children=[
        html.Div(map_plot_fees, className='column'),
        html.Div(map_plot_services, className='column'),
        html.Div(map_plot_providers, className='column')
    ]),
    html.Div(className='row', children=[
        html.Div(className='column'),
        html.Div(scatter_plot_states, className='column')
    ]),
    html.H3('Conclusion', className='row'),
    html.Div(
        'The plots above show that a difference in fees exists between the providers. The highest fee of 1.8% is '
        'charged by BKK VBU, the lowest fee of 0.8% is charged by BKK EUREGIO. An even bigger difference exists in the '
        'number of services offered: In the top rank, BERGISCHE KRANKENKASSE offers 152 different services, whereas at '
        'the bottom rank, BKK Diakonie only offers 57 different services. However for the reasons described above, the '
        'quality of the underlying dataset is unknown and the results should not be taken at face value without '
        'further validation. The differences at state level in average fees and number of services are negligible, '
        'however the number of available providers is slightly higher in the south of Germany than in the north. A '
        'correlation between fees charged and services offered does not seem to exist, neither at state level nor at '
        'the level of the individual providers.',
        className='row'
    ),
    html.Div(className='bottomrow')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

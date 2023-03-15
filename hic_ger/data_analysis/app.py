import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import json

providers_path = "hic_ger/data/providers_cleaned.csv"
states_path = "hic_ger/data/states_cleaned.csv"
states_map_path = "hic_ger/data/german_states.geo.json"
df_prov = pd.read_csv(providers_path, index_col=0)
df_states = pd.read_csv(states_path, index_col=0)

# Create bar plots
fig = px.bar(df_prov.sort_values('fee'), 'fee', 'name',
             title='Fees charged by each Provider',
             labels={'fee': 'Fee (%)'})
fig.update_yaxes(title_text='')
bar_plot_fees = dcc.Graph(id='bar plot fees', figure=fig, style={'height': '93vh'})
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
map_plot_providers = dcc.Graph(id='map plot providers', figure=fig_providers)

# Initialise the app
app = Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.H2('Statutory Health Insurance Companies in Germany', className='row'),
    html.H3('Introduction', className='row'),
    html.Div(
        [
            'This dashboard gives an overview about the fees charged by german statutory health insurance companies. '
            'The first part of the visualisations gives information '
            'on the individual companies (in the following called providers for reasons of brevity), whereas the '
            'second part accumulates the data on state level. The data on fees comes from the ',
            dcc.Link('german central association on statutory health insurance providers',
                  href='https://www.gkv-spitzenverband.de/service/krankenkassenliste/krankenkassen.jsp'),
            '. Statutory health insurance fees in Germany are determined by a fixed percentage of 14.6% of the '
            'customer\'s income. This base fee is independent of the provider. On top of that, each provider '
            'charges an additional fee that that is also determined by a percentage of the customer\'s income. These '
            'additional fees are the ones depicted in the visualizations below. '
        ],
        className='row'
    ),
    html.Div(className='column', children=[
        html.Div(bar_plot_fees)
    ]),
    html.Div(className='column', children=[
        html.Div(bar_plot_avgfees),
        html.Div(bar_plot_states)
    ]),
    html.Div(className='column', children=[
        html.Div(map_plot_fees),
        html.Div(map_plot_providers)
    ]),
    html.H3('Conclusion', className='row'),
    html.Div(
        'The plots above show that a difference in fees exists between the providers. The highest fee of 1.99% is '
        'charged by BKK Exklusiv, the lowest fee of 0.8% is charged by BKK Pfaff. The differences at state level in '
        'average fees are negligible, however the number of available providers is slightly higher in western Germany '
        'than in eastern Germany',
        className='row'
    ),
    html.Div(className='bottomrow')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px


providers_path = "../../data/providers_cleaned.csv"
states_path = "../../data/states_cleaned.csv"
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
pass


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
    html.Div('Graph area 2', className='column'),
    html.Div('Graph area 3', className='column')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
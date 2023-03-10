import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px


data_path = "../../data/data_cleaned.csv"
df = pd.read_csv(data_path)

# Create bar plots
fig = px.bar(df, 'fee', 'name')
bar_plot_fees = dcc.Graph(id='bar plot fees', figure=fig)
fig = px.bar(df, 'services_count', 'name')
bar_plot_services = dcc.Graph(id='bar plot services', figure=fig)


# Initialise the app
app = Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.H2('Health Insurance Comparison', className='row'),
    html.Div('Text Information', className='row'),
    html.Div(className='column', children=[
        html.Div(bar_plot_fees),
        html.Div(bar_plot_services)
    ]),
    html.Div('Graph area 2', className='column'),
    html.Div('Graph area 3', className='column')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
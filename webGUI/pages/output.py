import dash
from dash import html, dcc

dash.register_page(__name__, path="/output")

layout = html.Div([
    html.H1('Output'),
    html.Div([
        dcc.Markdown("This is our output page content. This will contain the link to export the data collected and measured and an interactive graph of the measurement itself."),
        ], style={'marginLeft': 50, 'marginRight': 50}),
])
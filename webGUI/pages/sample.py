import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div([
    html.H1('Sample'),
    html.Div([
        dcc.Markdown("This is our Sample page content. This will contain the link to export the data collected and measured and an interactive graph of the measurement itself."),
        ], style={'marginLeft': 50, 'marginRight': 50}),
])
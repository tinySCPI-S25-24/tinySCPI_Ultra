# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# press 'ctrl + C' to disconnect when completed

import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Remote Spectrum Analyzer Viewer', className="app-header--title")
        ]
    ),
    html.Div([
        html.A(
            dcc.Link(f"{page['name']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ], style={'textAlign': 'center', 'backgroundColor': "#cf4520"}),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
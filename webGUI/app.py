# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# press 'ctrl + C' to disconnect when completed

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

# Initialize Dash app with Bootstrap for modern styling
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

# Navbar Component
navbar = dbc.NavbarSimple(
    brand=html.Div("Remote Spectrum Analyzer Viewer", className="app-header--title"),
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"])) 
        for page in dash.page_registry.values()
    ],
    className="app-header"
)

# Footer Component
footer = html.Footer(
    children=[
        html.Img(src="/assets/logo.png", style={"width": "240px", "height": "auto"})
    ],
    className="app-footer"
)

# Layout with full-page flexbox structure
app.layout = html.Div([
    navbar,
    html.Div(dash.page_container, className="app-content"),
    footer
], className="app-container")

# Run the server
if __name__ == "__main__":
    app.run(debug=True)

import dash
from dash import html, dcc

dash.register_page(__name__, path="/about")

layout = html.Div(
    children=[
        html.H1('About'),
        html.Div(
            html.Img(src="/assets/tinysa_logo.jpg", style={"width": "25%", "height": "auto"}),
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "marginBottom": "30px"
            }
        ),
        html.Div([
            dcc.Markdown("""
                This is our About page content. It will contain an explanation on how to use the site and what it does. 
                It will also include a short explanation about what each automated measurement does and what files can be uploaded. 
                If needed, I will also add a FAQ page. There will also be a link to the source code.
            """),
        ], style={'marginLeft': 50, 'marginRight': 50, "textAlign": "center"}),
    ]
)
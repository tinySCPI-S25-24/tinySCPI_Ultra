import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1('  '),
    html.Div('Welcome! Please choose or upload your measurement below. If needed, please look in the "About" tab for further instructions.'),
    html.Div(
        className = "column",
        children=[
            html.Label('Select measurement and range of frequencies, or select "other" and upload custom script'),
            dcc.Dropdown(
                id='measurement-dropdown',
                options=[{'label': i, 'value': i} for i in ['1...', '2...', '3...', 'other']],
                placeholder="Select a measurement"
            ),
    ], style={'padding': 10, 'flex': 1}),

    html.Div(id='upload-container')
])

@callback(
    Output('upload-container', 'children'),
    Input('measurement-dropdown', 'value')
)
def show_upload(selected_value):
    if selected_value == 'other':
        return html.Div([
            html.Button("Upload Custom Script", id="upload-button"),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin-top': '10px'
                },
                multiple=False
            )
        ])
    return None

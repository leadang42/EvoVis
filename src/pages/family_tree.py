import dash
from dash import html

dash.register_page(__name__, path='/family-tree')

layout = html.Div([
    html.H1('Family Tree')
])
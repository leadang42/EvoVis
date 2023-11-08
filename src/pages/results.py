import dash
from dash import html

dash.register_page(__name__, path='/results')

col1a = html.Div([ html.H1("Results"), ], className="wrapper-col")
col1b = html.Div([ ], className="wrapper-col")

col2a = html.Div([ ], className="wrapper-col")
col2b = html.Div([ ], className="wrapper-col")

first_row = html.Div([ col1a, col1b ], className="wrapper")
second_row = html.Div([ col2a, col2b ], className="wrapper")

layout = html.Div([ first_row, second_row ], className="wrapper")
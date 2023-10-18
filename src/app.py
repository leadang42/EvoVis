import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from styles import PAGE_STYLE, SIDEBAR_STYLE
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY]) 

#sidebar = html.Div(
#    [
#        html.H3("EvoNAS", className="display-4"),
#        html.Hr(),
#       #html.P( "A simple sidebar layout with navigation links", className="lead" ),
#        dbc.Nav(
#            [
#                dbc.NavLink("Hyperparameter",  href=dash.page_registry['pages.hyperparameters']['relative_path'], active="exact"),
#                dbc.NavLink("Genepool", href=dash.page_registry['pages.genepool']['relative_path'], active="exact"),
#                dbc.NavLink("Results", href=dash.page_registry['pages.results']['relative_path'], active="exact"),
#                dbc.NavLink("Family Tree", href=dash.page_registry['pages.family_tree']['relative_path'], active="exact"),
#            ],
#            vertical=True,
#            pills=True,
#        ),
#    ],
#    style=SIDEBAR_STYLE,
#)

navbar = dbc.NavbarSimple(
    children=[
        dmc.NavLink(
            label="",
            icon=DashIconify(icon="mdi:github", height=25, color="#c2c7d0"),
            href="#",
            
        ),
        #dmc.NavLink(dbc.NavLink(" ", href="#", icon=DashIconify(icon="mdi:github", height=16, color="#c2c7d0"))),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Hyperparameter",  href=dash.page_registry['pages.hyperparameters']['relative_path']),
                dbc.DropdownMenuItem("Genepool", href=dash.page_registry['pages.genepool']['relative_path']),
                dbc.DropdownMenuItem("Results", href=dash.page_registry['pages.results']['relative_path']),
                dbc.DropdownMenuItem("Family Tree", href=dash.page_registry['pages.family_tree']['relative_path']),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

page = html.Div([dash.page_container], id="page-content", style=PAGE_STYLE)
app.layout = html.Div([dcc.Location(id="url"), navbar, page])

if __name__ == "__main__":
    app.run(debug=True)
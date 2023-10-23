import dash
from dash import html
import dash_cytoscape as cyto
from utils import get_ruleset

run = "ga_20230116-110958_sc_2d_4classes"

dash.register_page(__name__, path='/genepool')

# Header
col1a = html.Div([ html.H1("Genepool"), ], className="wrapper-col")
col1b = html.Div([ ], className="wrapper-col")
first_row = html.Div([ col1a], className="wrapper")

# Body
elements = get_ruleset(run)

cytoscape = cyto.Cytoscape(
    id='cytoscape-layout-1',
    elements=elements,
    style={'width': '100%', 'height': '800px'},
    layout={
            'name': 'breadthfirst',
            'roots': '#tha, #hall'
        }
)

#col2a = html.Div([cytoscape], className="wrapper-col")
#col2b = html.Div([ ], className="wrapper-col")
#second_row = html.Div([ col2a], className="wrapper")

layout = html.Div([ first_row, cytoscape ], className="wrapper")

import dash
from dash import html
import dash_cytoscape as cyto
from utils import get_family_tree

dash.register_page(__name__, path='/family-tree')

run = "ga_20230116-110958_sc_2d_4classes"

# Header
col1a = html.Div([ html.H1("Family Tree"), ], className="wrapper-col")
col1b = html.Div([ ], className="wrapper-col")
first_row = html.Div([ col1a ], className="wrapper")

# Body
elements = get_family_tree(run, 5, "important_chital", None)

cytoscape = cyto.Cytoscape(
    id='cytoscape-layout-1',
    elements=elements,
    style={'width': '100%', 'height': '800px'},
    layout={
        'name': 'breadthfirst',
        'roots': '[id = "hal"]'
    }
)

#col2a = html.Div([ ], className="wrapper-col")
#col2b = html.Div([ ], className="wrapper-col")
#second_row = html.Div([ col2a, col2b ], className="wrapper")

layout = html.Div([ first_row, cytoscape ], className="wrapper")

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
individual = 'important_chital'
elements, roots = get_family_tree(run, 5, individual, range(2, 6))

cytoscape_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#6173E9',
            'content': 'data(label)',
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#6173E9',
        }
    }, 
    {
        'selector': 'label',
        'style': {
            'color': '#6173E9',
            'text-background-color': '#FFFFF3',
        }
    },
    {
        'selector': f'[id = "{individual}"]',
        'style': {
            'background-color': '#8BC267',
            'content': 'data(label)'
        }
    },
]

cytoscape = cyto.Cytoscape(
    id='cytoscape-family-tree',
    elements=elements,
    style={'width': '100%', 'height': '550px'},
    stylesheet=cytoscape_stylesheet,
    layout={
        'name': 'breadthfirst',
        'roots': roots
    }
)

#col2a = html.Div([ ], className="wrapper-col")
#col2b = html.Div([ ], className="wrapper-col")
#second_row = html.Div([ col2a, col2b ], className="wrapper")

layout = html.Div([ first_row, cytoscape ], className="wrapper")

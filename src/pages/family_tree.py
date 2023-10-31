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
            'width':'50px',
            'height':'50px',
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
            'font-family': 'sans-serif',
            'color': '#FFFFFF',
            'font-size': '12px',
            'font-weight': 'bold',
            'text-valign': 'center',
        }
    },
    {
        'selector': f'[id = "{individual}"]',
        'style': {
            'background-color': '#FFFFFF',
            'border-color': '#6173E9',
            'border-width': '3px',
            'content': 'data(label)',
            'color': '#000000', # Font color
        }
    },
]

cytoscape = cyto.Cytoscape(
    id='cytoscape-family-tree',
    elements=elements,
    style={'width': '550px', 'height': '550px'},
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

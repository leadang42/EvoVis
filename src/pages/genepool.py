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

cytoscape_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#6173E9',
            #'background-color': '#EFEFEF',
            #'border-color': '#6173E9',
            #'border-width': '3px',

            'content': 'data(label)',
            'width':'50px',
            'height':'50px'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#6173E9'
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
        'selector': '[id = "Start"]',
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
    id='cytoscape-genepool',
    elements=elements,
    style={'height': '550px', 'max-width': '800px'},
    stylesheet=cytoscape_stylesheet,
    layout={
            'name': 'cose',
        }
)

#col2a = html.Div([cytoscape], className="wrapper-col")
#col2b = html.Div([ ], className="wrapper-col")
#second_row = html.Div([ col2a], className="wrapper")

layout = html.Div([ first_row, cytoscape ], className="wrapper")

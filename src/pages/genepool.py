import dash
from dash import html, Input, Output, callback
import dash_cytoscape as cyto
from utils import get_ruleset, get_start_gene
from components import metric_card, dot_heading
import json

run = "ga_20230116-110958_sc_2d_4classes"
dash.register_page(__name__, path='/genepool')

# Ruleset of evonas run
elements = get_ruleset(run)

# Header
numb_genes = 500
dimension = "2D"
gene = "STFT"

row1a = html.Div( [ html.H1("Genepool")], className="wrapper")
row1b = html.Div(
    [ html.Div([

        html.Img(src="assets/media/gene-background.png", height="250px", width="600px"),
        html.Div([f"#{numb_genes}"], className="top-left"),
        html.Div([gene], className="center-left", id="gene-name"),
        html.Div([dimension], className="bottom-center"),],

    className="image-text-container",)], 
    className="wrapper"
)
row1c = html.Div(
    [
        metric_card("padding", 'val', "fluent:memory-16-regular", width="285px"),
        metric_card("kernel", 'val', "uiw:time-o", width="285px"),
        metric_card("pooling", 'val', "simple-line-icons:energy", width="285px"),
        metric_card("pooling", 'val', "simple-line-icons:energy", width="285px"),
    ],
    className="wrapper",
    style={'width':'600px'}
)

first_col = html.Div([row1a, row1b, row1c, ], className="wrapper-col")

# Body
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
    style={'height': '550px', 'width':'50%','display': 'inline-block', 'margin-top':'70px'},
    stylesheet=cytoscape_stylesheet,
    layout={
            'name': 'cose',
        }
)

# Cytoscape interactions
@callback(Output('gene-name', 'children'), Input('cytoscape-genepool', 'tapNodeData'))
def displayTapNodeData(data):
    if data is None:
        get_start_gene(run)["f_name"]

    return data["id"]


layout = html.Div([ first_col, cytoscape], className="wrapper")

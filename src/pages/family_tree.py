import dash
from dash import html, callback, Input, Output
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import get_family_tree, get_generations, get_individuals

dash.register_page(__name__, path='/family-tree')

run = "ga_20230116-110958_sc_2d_4classes"

# Header
col1a = html.Div([ html.H1("Family Tree"), ], className="wrapper-col")
col1b = html.Div([ ], className="wrapper-col")
first_row = html.Div([ col1a ], className="wrapper")

# Generation Selection
gen_select = dmc.Select(
    label="Select Generation",
    placeholder="Select Generation",
    icon=DashIconify(icon="material-symbols-light:circle", height=10, width=10, color="#6173E9"),
    data=[{"value": gen, "label": gen.replace("_", " ")} for gen in get_generations(run)],
    id="gen-select",
    className="circle-select",
)

@callback( output=Output("ind-select", "data"), inputs=Input("gen-select", "value") )
def get_gen(gen):
    gen = int(gen.split("_")[1])
    return [{"value": ind, "label": ind.replace("_", " ")} for ind in get_individuals(run, generation_range=range(gen, gen+1), value="name", as_generation_dict=False)]

# Individual Selection
ind_select = dmc.Select(
    label="Select Individual",
    placeholder="Select Individual",
    icon=DashIconify(icon="material-symbols-light:circle", height=10, width=10, color="#6173E9"),
    data=[{"value": ind, "label": ind.replace("_", " ")} for ind in get_individuals(run, generation_range=range(5,6), value="name", as_generation_dict=False)],
    id="ind-select",
    className="circle-select",
)

@callback( 
    Output("cytoscape-family-tree", "elements"), 
    Output("cytoscape-family-tree", "layout"), 
    Input("gen-select", "value"),
    Input("ind-select", "value") 
)
def get_ind(gen, ind):
    gen = int(gen.split("_")[1])
    elements, roots = get_family_tree(run, gen, ind, range(gen-3, gen+2))
    return elements, { 'name': 'breadthfirst', 'roots': roots }

node_select = dmc.Grid(
    children=[
        dmc.Col(gen_select, span="auto"),
        dmc.Col(ind_select, span="auto"),
    ],
    justify="center",
    gutter="sm",
)

# Cytoscape 
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
        'selector': f'[id = ""]',
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
    style={'height': '500px'},
    stylesheet=cytoscape_stylesheet,
)

#layout = html.Div([ first_row, generation_div, individual_div, cytoscape ])

layout = dmc.Grid(
    children=[
        dmc.Col(html.Div([ first_row, node_select, cytoscape ]), span=5),
        dmc.Col(html.Div([]), span="auto"),
    ],
    gutter="s",
    justify="space-between",
)
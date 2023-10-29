import dash
from dash import html, Input, Output, callback, dcc
import dash_cytoscape as cyto
import json
import re
import plotly.express as px
import pandas as pd

from utils import get_ruleset, get_start_gene, get_number_of_genes, get_generations
from components import metric_card, dot_heading

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
)

row1c = html.Div( [], style={'width':'600px'}, id="metric-cards-section")

row1d = html.Div( [], style={'width':'600px'}, id="number-of-genes", className="wrapper")

first_col = html.Div([row1a, row1b, row1c, row1d], className="wrapper-col")

# Body
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
            #'target-arrow-color': '#6173E9',
            #'target-arrow-shape': 'chevron'
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
    style={'height': '600px', 'width':'50%','display': 'inline-block', 'margin-top':'70px'},
    stylesheet=cytoscape_stylesheet,
    layout={
            'name': 'cose',
        }
)

# Cytoscape interactions
@callback(
    Output('gene-name', 'children'), 
    Output('metric-cards-section', 'children'), 
    Output('number-of-genes', 'children'),
    Output('cytoscape-genepool', 'stylesheet'),
    
    Input('cytoscape-genepool', 'tapNodeData'))
def displayTapNodeData(data):
    
    gene = data
    
    if data is None:
        gene = get_start_gene(run)
        print(gene)
    
    # Gene name
    gene_name = gene["f_name"].replace("()", "").replace("2D", "").replace("1D", "").replace("Conv", "Convolution").replace("STFT", "Short Time Fourier Trans.")
    gene_name = ' '.join(re.findall('[A-Z][a-z]*', gene_name)).replace("Re L U", "ReLU")
    
    # Metric cards
    metric_cards = []
    for key, value in gene.items():
        
        if str(key) != "id" and str(key) != "label" and str(key) != "f_name" and key != "layer":
            
            mc = metric_card(key, str(value), "mdi:input", width="290px")
            metric_cards.append(mc)   
            
    # Number of genes per generation
    numb_of_genes = []
    for generation in range(1, len(get_generations(run))+1):
        numb_of_genes.append(get_number_of_genes(run, generation, gene["layer"]))
    
    df = pd.DataFrame({"x": list(range(1, len(get_generations(run))+1)), "y": numb_of_genes})
    fig = px.bar(x = list(range(1, len(get_generations(run))+1)), y = numb_of_genes, labels={"x": "Generation", "y": f"{gene['layer']} layers"})
    graph = dcc.Graph(figure=fig, style={'width':'585px', 'height':'200px'})
    
    fig.update_layout(
        plot_bgcolor='white'
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
            
    # New node style when node is clicked
    cytoscape_stylesheet_copy = cytoscape_stylesheet.copy()
    cytoscape_stylesheet_copy.append({
        'selector': f'[id = "{gene["layer"]}"]',
        'style': {
            'background-color': '#CD3B3B',
            'border-color': '#CD3B3B',
            'border-width': '3px',
            'content': 'data(label)',
            'color': '#FFFFFF', # Font color
        }})
    
    cytoscape_stylesheet_copy.append({
        'selector': f'.{gene["layer"]}',
        'style': {
            'line-color': '#CD3B3B',
            #'line-fill': 'radial-gradient'
        }})
    
    return gene_name, metric_cards, graph, cytoscape_stylesheet_copy


layout = html.Div([ first_col, cytoscape], className="wrapper")

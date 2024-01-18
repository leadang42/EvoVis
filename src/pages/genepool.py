import dash
from dash import html, Input, Output, callback, dcc
import dash_cytoscape as cyto
import re
import plotly.express as px
import pandas as pd
from utils import get_number_of_genes, get_generations
from search_space import get_cytoscape_elements
from components import metric_card

run = "ga_20230116-110958_sc_2d_4classes"

dash.register_page(__name__, path='/genepool')

# Header
row1a = html.Div( [ html.H1("Genepool")], className="wrapper")
row1b = html.Div(
    [ html.Div([

        html.Img(src="assets/media/gene-background.png", height="250px", width="600px"),
        html.Div([], className="top-left", id="gene-amount"),
        html.Div([], className="center-left", id="gene-name"),
        html.Div([], className="bottom-center", id="gene-type"),],

    className="image-text-container",)], 
)

row1c = html.Div( [], style={'width':'600px'}, id="metric-cards-section", className="wrapper")

row1d = html.Div( [], style={'width':'600px'}, id="number-of-genes-graph", className="wrapper")

first_col = html.Div([row1a, row1b, row1c, row1d], className="wrapper-col")

# Body

elements, groups = get_cytoscape_elements("ga_20240108-231402_spoken_languages")
    
def cytoscape_stylesheet(groups):
    
    # Style for layer nodes and egdes and class edges
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
                'width': '2px'
            }
        },
        {
            'selector': 'label',
            'style': {
                'font-family': 'sans-serif',
                'color': '#FFFFFF',
                'font-size': '12px',
                'font-weight': '500',
                'text-valign': 'center',
            }
        },
        {
            'selector': '[id = "Start"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '2px',
                'content': 'data(label)',
                'color': '#000000', # Font color
            }
        },
        {
            'selector': '[id = "end"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '2px',
                'content': 'data(label)',
                'color': '#000000', # Font color
            }
        },
        {
            'selector': '[id = "class-connect"]',
            'style': {
                'width': '2px',
                'line-color': '#6173E9',
            }
        },
    ]

    # Style for groupe nodes
    for group in groups:
    
        group_node_style = {
            'selector': f'[id = "{group}"]',
            'style': {
                #Box
                'background-fill': 'radial-gradient', 
                'background-gradient-stop-colors': '#EFEFEF #6173E9',
                'background-gradient-stop-positions': '0% 50%',
                'background-opacity': '0.5',
                'shape': 'round-rectangle',
                'border-color': '#6173E9',
                'border-width': '2px',
                'width':'400px',
                'height':'400px',
                #Font
                'color': '#6173E9',
                'text-background-color': '#FFFFFF',
                'text-background-shape': 'round-rectangle',
                'text-background-padding': '5px',
                'text-background-opacity': '1',
                'text-border-color':'#6173E9',
                'text-border-opacity':'1',
                'text-border-width': '1px',
                'text-valign': 'bottom',
                'line-height': '10',
                'font-size': '15px',
            }
        }

        cytoscape_stylesheet.append(group_node_style)
    
    return cytoscape_stylesheet

def cytoscape_search_space():
    
    # Create stylesheet with different styling of groups
    stylesheet = cytoscape_stylesheet(groups)
    
    cytoscape = cyto.Cytoscape(
        id='cytoscape-genepool',
        elements=elements,
        style={'height': '600px', 'width':'50%', 'display': 'inline-block', 'margin-top':'70px'},
        stylesheet=stylesheet,
        layout={
            'name': 'cose',
        }
    )
    
    return cytoscape

# Cytoscape interactions
@callback(
    Output('gene-name', 'children'), 
    Output('gene-amount', 'children'),
    Output('gene-type', 'children'),
    Output('metric-cards-section', 'children'), 
    Output('number-of-genes-graph', 'children'),
    Output('cytoscape-genepool', 'stylesheet'),
    
    Input('cytoscape-genepool', 'tapNodeData'))
def display_node_data(data):
    
    gene = data
    
    if data is None:
        gene = {'id': 'Start', 'label': 'Start', 'f_name': 'Start', 'layer': 'Start', 'parent': 'Starting point'}
    
    # Gene name
    gene_name = gene["f_name"].replace("()", "").replace("2D", "").replace("1D", "").replace("Conv", "Convolution").replace("STFT", "Short Time Fourier Trans.")
    gene_name = ' '.join(re.findall('[A-Z][a-z]*', gene_name)).replace("Re L U", "ReLU")
    
    # Gene dimension
    gene_type = ""
    if "parent" in gene:
        gene_type = gene["parent"]
    
    # Metric cards
    metric_cards = []
    for key, value in gene.items():
        
        not_metric = ["id", "label", "f_name", "layer", "parent", "exclude"]
        
        if key not in not_metric:
            
            mc = metric_card(key, str(value), "mdi:input", width=282)
            metric_cards.append(mc)   
            
    # Number of genes per generation
    numb_of_genes = []
    for generation in range(1, len(get_generations(run))+1):
        numb_of_genes.append(get_number_of_genes(run, generation, gene["layer"]))
    
    df = pd.DataFrame({"x": list(range(1, len(get_generations(run))+1)), "y": numb_of_genes})
    fig = px.bar(x = list(range(1, len(get_generations(run))+1)), y = numb_of_genes, labels={"x": "Generation", "y": f"{gene['layer']} layers"})
    graph = dcc.Graph(figure=fig, style={'width':'585px', 'height':'150px'})
    
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        font_color="black",
    )
    fig.update_xaxes(
        title_standoff=10
    )
    fig.update_yaxes(
        title_standoff=10
    )
    
    # Amount of genes
    gene_amount = 0
    
    for numb_gen in numb_of_genes:
        gene_amount += numb_gen
        
    gene_amount = f"{gene_amount} Count"
            
    # New node style when node is clicked
    cytoscape_stylesheet_copy = cytoscape_stylesheet(groups)
    
    cytoscape_stylesheet_copy.append({
        'selector': f'[id = "{gene["layer"]}"]',
        'style': {
            'background-color':  '#6173E9',
            'border-color': '#FFFFFF',
            'border-width': '2px',
            'content': 'data(label)',
            'color': '#FFFFFF',
        }})
    
    cytoscape_stylesheet_copy.append({
        'selector': f'.{gene["layer"]}',
        'style': {
            'line-color': '#FFFFFF',
        }})
    
    return gene_name, gene_amount, gene_type, metric_cards, graph, cytoscape_stylesheet_copy


layout = html.Div([ first_col, cytoscape_search_space()], className="wrapper")

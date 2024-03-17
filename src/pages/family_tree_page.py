import dash
from dash import html, callback, Input, Output, dcc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dotenv import load_dotenv
import os
from evolution import get_family_tree, get_generations, get_individuals, get_random_individual, get_individuals_min_max, get_individual_result, get_individual_chromosome, get_meas_info
from components import dot_heading, bullet_chart_card, bullet_chart_card_basic, warning, information, chromosome_sequence
from dataval import validate_generations_of_individuals, validate_crossover_parents

### LOAD PATH FROM ENVIRONMENT VARIABLES
load_dotenv()
run = os.getenv("RUN_RESULTS_PATH")


### REGISTER DASH APP
dash.register_page(__name__, path='/family-tree')


### GLOBAL VARIABLES 
GENERATIONS = get_generations(run)
GENERATIONS_INT = get_generations(run, as_int=True)
RANDOM_GENERATION, _ = get_random_individual(run, 5)
BORDER_MEAS = get_individuals_min_max(run, generation_range=None)
MEAS_INFO = get_meas_info(run)
del MEAS_INFO['fitness']
CYTOSCAPE_STYLE = [
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
            'label': 'data(edgelabel)',
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
        'selector': 'edgelabel',
        'style': {
            'font-family': 'sans-serif',
            'color': '#FFFFFF',
            'font-size': '12px',
            'font-weight': 'bold',
            'text-valign': 'center',
            'text-background-color': '#6173E9',
            'text-background-opacity': '0.5',
            'text-background-shape': 'round-rectangle',
            'text-background-padding': '5px'
        }
    },
]
MARKS_STYLE = {
    'color': '#6173E9', 
    'background-color': '#D1D6F8', 
    'padding': '2px', 
    'border-radius': '3px',
    'font-size': '12px',
    'font-weight': '300',
}


### FAMILY TREE COMPONENTS 
def family_tree_cytsocape():
    return cyto.Cytoscape(
        id='cytoscape-family-tree',
        className="wrapper",
        style={'height': '450px', 'max-width': '100%'},
        stylesheet=CYTOSCAPE_STYLE,
    )

def generation_slider():
    return dcc.RangeSlider(
        min(GENERATIONS_INT), 
        max(GENERATIONS_INT), 
        1, 
        marks={
            min(GENERATIONS_INT): {"label": f"Generation_{min(GENERATIONS_INT)}", "style": MARKS_STYLE}, 
            max(GENERATIONS_INT): {"label": f"Generation_{max(GENERATIONS_INT)}", "style": MARKS_STYLE}
        }, 
        #pushable=1, 
        allowCross=False,
        id='gen-range-slider',
        tooltip={"placement": "top", "always_visible": True},
        value=[RANDOM_GENERATION-3, RANDOM_GENERATION, RANDOM_GENERATION+1], 
    )

def individual_select(): 
    return dmc.Select(
        label="Select Individual",
        placeholder="Select Individual",
        icon=DashIconify(icon="material-symbols-light:circle", height=10, width=10, color="#6173E9"),
        id="ind-select",
        className="circle-select",
    )


### FAMILY TREE MODIFICATION CALLBACKS 
@callback( Output("ind-select", "data"), Output("ind-select", "value"), Input("gen-range-slider", "value"))
def set_individuals_select(gen_range):
    gen = gen_range[1]
    
    data = [{"value": ind, "label": ind} for ind in get_individuals(run, generation_range=range(gen, gen+1), value="names", as_generation_dict=False)]
    gen, value = get_random_individual(run, generation=gen)
    
    return data, value

@callback( Output("cytoscape-family-tree", "elements"), Output("cytoscape-family-tree", "layout"), Output("cytoscape-family-tree", "stylesheet"), Input("gen-range-slider", "value"), Input("ind-select", "value"), Input("cytoscape-family-tree", "tapNodeData"), Input("cytoscape-family-tree", "tapEdgeData"))
def set_cytoscape(gen_range, ind, ind_clicked, edge_clicked):
    
    # Get Family tree through individual selection
    generation_range = range(gen_range[0], gen_range[2]+1)
    gen = gen_range[1]
    elements, roots = get_family_tree(run, gen, ind, generation_range)
    
    cytoscape_layout = {
        'name': 'breadthfirst', 
        'roots': roots
    }
    
    # Creating new stylesheet with white selected node
    new_cytoscape_style = CYTOSCAPE_STYLE.copy()

    # Add styling for 
    if ind is not None: 
        new_cytoscape_style.append({
            'selector': f'[id = "{ind}"]',
            'style': {
                'background-color': '#6173E9',
                'border-color': '#FFFFFF',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#FFFFFF',
            }, 
        })
    
    if ind_clicked is not None: 
        ind_clicked_id = ind_clicked['id']
        
        new_cytoscape_style.append({
            'selector': f'[id = "{ind_clicked_id}"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#000000',
            }
        })   
        
    if edge_clicked is not None: 
        edge_id = edge_clicked['id']
        source = edge_clicked['source']
        target = edge_clicked['target']

        new_cytoscape_style.append({
            'selector': f'[id = "{source}"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#000000',
            }
        }) 
        
        new_cytoscape_style.append({
            'selector': f'[id = "{target}"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#000000',
            }
        }) 
    
    return elements, cytoscape_layout, new_cytoscape_style

@callback( 
    Output("individual-heading", "children"),  Output("individual-exceptions", "children"), Output("individual-genes", "children"), Output("individual-results", "children"), 
    Input("cytoscape-family-tree", "tapNodeData"), Input("ind-select", "value"), Input("gen-range-slider", "value"))
def set_values(ind_clicked, ind_select, gen_range):
    
    # Individual selected in cytoscape
    ind = None
    gen = None
    extinct = None
    
    if ind_clicked is None: 
        ind = ind_select
        gen = gen_range[1]
        extinct = False
    
    else:
        ind = ind_clicked["id"]
        gen = ind_clicked["generation"]
        extinct = ind_clicked["extinct"]
        
    # Get individual information from selected node
    ind_meas = get_individual_result(run, gen, ind)
    ind_genome = get_individual_chromosome(run, gen, ind)
        
    ### 1 HEADING ###
    ind_heading = [html.H2(ind, style = {'margin': '10px'})]
    
    ### 2 EXCEPTIONS ###
    ind_exceptions = []

    if extinct:
        ind_exceptions.append(information("Individual became extinct."))

    if "error" in ind_meas and (ind_meas["error"] == "True" or ind_meas["error"] == True):
        ind_exceptions.append(warning("Individual errored."))

    ### 3 CHROMOSOME ###
    ind_genes = [dot_heading("Genes", style={"margin": "10px",'flex': '100%'}), chromosome_sequence(chromosome=ind_genome)]
    
    ### 4 RESULTS ###
    ind_fitness = [dot_heading("Fitness", style={"margin": "10px",'flex': '100%'})]
    
    if "fitness" in ind_meas:
        ind_fitness += [bullet_chart_card_basic(ind_meas['fitness'], 0, 1, metric_card_id="bullet-chart-basic")]

    for meas_key in list(MEAS_INFO.keys()):
        if meas_key in ind_meas:
            
            if isinstance(ind_meas[meas_key], (float, int)):
                
                ind_fitness += [(
                    bullet_chart_card(
                        MEAS_INFO[meas_key]["displayname"], 
                        MEAS_INFO[meas_key]["individual-info-img"], 
                        ind_meas[meas_key], 
                        BORDER_MEAS[meas_key][0], 
                        BORDER_MEAS[meas_key][1], 
                        unit=MEAS_INFO[meas_key]["unit"], 
                        constraint=None, 
                        metric_card_id="bullet-chart-card"
                    )
                )]
            
    return ind_heading, ind_exceptions, ind_genes, ind_fitness


### FAMILY TREE PAGE LAYOUT  
def family_tree_header():
    return html.H1('Family Tree', style = {"margin-bottom": "20px", "margin-top": "20px"})

def family_tree():
    return dmc.Col(html.Div(
        [ 
            family_tree_header(), 
            individual_select(), 
            family_tree_cytsocape(),
            generation_slider()
        ]), 
        span='auto',
        style={'max-width': '100%'} 
    )
    
def individual_information():
    return dmc.Col(
        [
            html.Div([], id='individual-heading'), 
            html.Div([], id='individual-exceptions'), 
            dmc.Grid(
                [
                    dmc.Col([html.Div([], id='individual-results')], span=10),
                    dmc.Col([html.Div([], id='individual-genes')], span='auto')
                ],
                gutter="xs",
                grow=True
            )
        ], 
        span=2, 
        className='cytoscape-values', 
        id='values-col'
    )

def family_tree_layout():
    
    validation_result = validate_generations_of_individuals(run) + validate_crossover_parents(run)
    layout = None
    
    if validation_result:
        layout=html.Div(
            children=[
                family_tree_header(),
                warning(validation_result)
            ]
        )
        print(validation_result)
        
    else:
        layout = dmc.Grid(
            children=[
                family_tree(),
                individual_information()
            ],
            gutter="s",
            grow=True
        )
    
    return layout

layout = family_tree_layout
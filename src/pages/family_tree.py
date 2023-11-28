import dash
from dash import html, callback, Input, Output, dcc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import random

from utils import get_family_tree, get_generations, get_individuals, get_random_individual, get_individuals_min_max, get_individual_result, get_individual_chromosome, get_hyperparamters
from components import dot_heading, bullet_chart_card, bullet_chart_basic, warning, information

dash.register_page(__name__, path='/family-tree')

### GLOBAL VARIABLES ###
run = "ga_20230116-110958_sc_2d_4classes"
generations = get_generations(run)
generations_int = get_generations(run, as_int=True)

random_gen, random_ind = get_random_individual(run, generation=5) #ethereal_puma?? #5, "premium_capuchin"

border_meas = get_individuals_min_max(run, generation_range=None)


### CYTOSCAPE ###
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

cytoscape = cyto.Cytoscape(
    id='cytoscape-family-tree',
    className="wrapper",
    style={'height': '300px'},
    stylesheet=cytoscape_stylesheet,
)

### FAMILY TREE MODIFICATION COMPONENTS ###
slider = dcc.RangeSlider(
    min(generations_int), 
    max(generations_int), 
    1, 
    #marks=None, 
    #pushable=1, 
    allowCross=False,
    id='gen-range-slider',
    tooltip={"placement": "bottom", "always_visible": False},
    value=[random_gen-3, random_gen, random_gen+1], 
)

gen_select = dmc.Select(
    label="Select Generation",
    placeholder="Select Generation",
    icon=DashIconify(icon="material-symbols-light:circle", height=10, width=10, color="#6173E9"),
    id="gen-select",
    className="circle-select",
    data=[{"value": gen, "label": gen.replace("_", " ")} for gen in generations],
    value=f"Generation_{random_gen}",
)

ind_select = dmc.Select(
    label="Select Individual",
    placeholder="Select Individual",
    icon=DashIconify(icon="material-symbols-light:circle", height=10, width=10, color="#6173E9"),
    id="ind-select",
    className="circle-select",
)

node_select = dmc.Grid(
    children=[
        dmc.Col(gen_select, span="auto"),
        dmc.Col(ind_select, span="auto"),
    ],
    justify="center",
    gutter="sm",
)


### FAMILY TREE MODIFICATION CALLBACKS ###
@callback( Output("ind-select", "data"), Output("ind-select", "value"), Input("gen-select", "value") )
def set_individuals_select(gen):
    gen = int(gen.split("_")[1])
    
    data = [{"value": ind, "label": ind.replace("_", " ")} for ind in get_individuals(run, generation_range=range(gen, gen+1), value="names", as_generation_dict=False)]
    gen, value = get_random_individual(run, generation=gen)
    
    return data, value


@callback(Output("gen-select", "value"), Input("gen-range-slider", "value"))
def set_generation_select(gen_range):
    return f"Generation_{gen_range[1]}"


@callback(Output("gen-range-slider", "value"), Input("gen-range-slider", "value"), Input("gen-select", "value"))
def set_generation_range(gen_range, gen):
    gen = int(gen.split("_")[1])
    
    if gen_range[1] != gen:
        return [gen-3, gen, gen+1]
    
    else:
        return gen_range


@callback( Output("cytoscape-family-tree", "elements"), Output("cytoscape-family-tree", "layout"), Output("cytoscape-family-tree", "stylesheet"), Input("gen-range-slider", "value"), Input("gen-select", "value"), Input("ind-select", "value"))
def set_cytoscape(gen_range, gen, ind):
    
    generation_range = range(gen_range[0], gen_range[2]+1)
    gen = gen_range[1] #int(gen.split("_")[1])
    
    elements, roots = get_family_tree(run, gen, ind, generation_range)
    
    # Creating new stylesheet with white selected node
    new_cytoscape_stylesheet = cytoscape_stylesheet.copy()
    
    new_cytoscape_stylesheet.append({
        'selector': f'[id = "{ind}"]',
        'style': {
            'background-color': '#FFFFFF',
            'border-color': '#6173E9',
            'border-width': '3px',
            'content': 'data(label)',
            'color': '#000000',
        }
    })
    
    return elements, { 'name': 'breadthfirst', 'roots': roots }, new_cytoscape_stylesheet


@callback( Output("individual-heading", "children"),  Output("individual-exceptions", "children"), Output("individual-genes", "children"), Output("individual-results", "children"), Input("cytoscape-family-tree", "tapNodeData"))
def set_values(ind_clicked):
    
    print(ind_clicked)
    
    # No node clicked
    if ind_clicked is None: 
        return [], [], [], []
    
    # Individual information
    ind = ind_clicked["id"]
    gen = ind_clicked["generation"]
    extinct = ind_clicked["extinct"]
    
    meas_keys = ["memory_footprint_h5", "memory_footprint_tflite", "memory_footprint_c_array", "val_acc", "inference_time", "energy_consumption"]
    ind_meas = get_individual_result(run, gen, ind)
    ind_genome = get_individual_chromosome(run, gen, ind)
    hyperparameters = get_hyperparamters(run)
    
    meas_info = {
        'memory_footprint_h5': ('Byte', hyperparameters['max_memory_footprint']),
        'memory_footprint_tflite': ('Byte', None),
        'memory_footprint_c_array': ('Byte', None),
        'val_acc': ('', None),
        'inference_time': ('ms', hyperparameters['max_inference_time']),
        'energy_consumption': ('mJ', hyperparameters['max_energy_consumption']),
    }
    
    print("No problem here")
    
    # Creating heading div
    ind_heading = [html.H2(ind.replace('_', ' '), style = {'margin': '10px'})]
    
    # Creating exceptions div
    ind_exceptions = []
    
    if extinct:
        ind_exceptions += [information("Individual became extinct.")]
        
    if "energy_consumption" in ind_meas and "inference_time" in ind_meas:
        if (type(ind_meas["energy_consumption"]) != int and type(ind_meas["energy_consumption"]) != float) or (type(ind_meas["inference_time"]) != int and type(ind_meas["inference_time"]) != float):            
            return ind_heading, warning("Measuring energy consumption failed with this individual"), [], []
    else: 
        return ind_heading, warning("Measuring energy consumption failed with this individual"), [], []
    
    # Creating genes values
    ind_genes = [dot_heading("Genome", style={"margin": "10px",'flex': '100%'})]
    
    for gene in ind_genome:
        
        gene_params = str(gene)
        gene_params = gene_params.replace('{}', '').replace('}', '').replace("'", '')
        
        tooltip = dmc.Tooltip(
            label=gene_params,
            position="right",
            offset=3,
            transition="slide-up",
            color='gray',
            multiline=True,
            children=[dmc.Badge(gene["layer"].replace('_', ''), variant='light', color='indigo', style={'flex': '100%'})]
        )
        ind_genes.append(tooltip)
    
    # Creating fitness values
    ind_fitness = [dot_heading("Fitness", style={"margin": "10px",'flex': '100%'})]
    
    if "fitness" in ind_meas:
        ind_fitness += [bullet_chart_basic(ind_meas['fitness'], 0, 1, metric_card_id="bullet-chart-basic")]

    for meas_key in meas_keys:
        if meas_key in ind_meas:
            if meas_key == 'inference_time':
                ind_fitness += [(bullet_chart_card(meas_key.replace("_", " "), f"{meas_key.replace('_', '-')}-icon", ind_meas[meas_key], border_meas[meas_key]['min']['value'], 300, unit=meas_info[meas_key][0], constraint=meas_info[meas_key][1], metric_card_id="bullet-chart-card"))]
            elif meas_key == 'energy_consumption':
                ind_fitness += [(bullet_chart_card(meas_key.replace("_", " "), f"{meas_key.replace('_', '-')}-icon", ind_meas[meas_key], border_meas[meas_key]['min']['value'], 5, unit=meas_info[meas_key][0], constraint=meas_info[meas_key][1], metric_card_id="bullet-chart-card"))]
            else:
                ind_fitness += [(bullet_chart_card(meas_key.replace("_", " "), f"{meas_key.replace('_', '-')}-icon", ind_meas[meas_key], border_meas[meas_key]['min']['value'], border_meas[meas_key]['max']['value'], unit=meas_info[meas_key][0], constraint=meas_info[meas_key][1], metric_card_id="bullet-chart-card"))]
    
    return ind_heading, ind_exceptions, ind_genes, ind_fitness


### LAYOUT ###

layout = dmc.Grid(
    children=[
        dmc.Col(html.Div(
            [ 
                html.H1("Family Tree", className="wrapper", style = {"margin-bottom": "20px", "margin-top": "20px"}), 
                node_select, 
                cytoscape,
                slider
            ]), 
            span=4
        ),
        dmc.Col([
            html.Div([], id='individual-heading'), 
            html.Div([], id='individual-exceptions'), 
            dmc.Grid(
                [dmc.Col([html.Div([], id='individual-genes')], span=2),
                dmc.Col([html.Div([], id='individual-results')], span='auto')],
                gutter="xs",
            )], 
            span="auto", 
            className='cytoscape-values', 
            id='values-col'),
    ],
    gutter="s",
    justify="space-between",
)
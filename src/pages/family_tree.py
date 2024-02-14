import dash
from dash import html, callback, Input, Output, dcc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import get_family_tree, get_generations, get_individuals, get_random_individual, get_individuals_min_max, get_individual_result, get_individual_chromosome, get_meas_info
from components import dot_heading, bullet_chart_card, bullet_chart_basic, warning, information, genome_overview

dash.register_page(__name__, path='/family-tree')

### GLOBAL VARIABLES ###
run = "ga_20240108-231402_spoken_languages"
run = "nRF52840"

generations = get_generations(run)
generations_int = get_generations(run, as_int=True)
random_gen, _ = get_random_individual(run, 5)
border_meas = get_individuals_min_max(run, generation_range=None)

# TODO Meas infor from config
meas_info = get_meas_info(run)
del meas_info['fitness']

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
    style={'height': '300px', 'max-width': '100%'},
    stylesheet=cytoscape_stylesheet,
)

### FAMILY TREE MODIFICATION COMPONENTS ###
slider = dcc.RangeSlider(
    min(generations_int), 
    max(generations_int), 
    1, 
    marks=None, 
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


@callback( Output("cytoscape-family-tree", "elements"), Output("cytoscape-family-tree", "layout"), Output("cytoscape-family-tree", "stylesheet"), Input("gen-range-slider", "value"), Input("gen-select", "value"), Input("ind-select", "value"), Input("cytoscape-family-tree", "tapNodeData"), Input("cytoscape-family-tree", "tapEdgeData"))
def set_cytoscape(gen_range, gen, ind, ind_clicked, edge_clicked):
    
    # Get Family tree through individual selection
    generation_range = range(gen_range[0], gen_range[2]+1)
    gen = gen_range[1]
    elements, roots = get_family_tree(run, gen, ind, generation_range)
    
    cytoscape_layout = {
        'name': 'breadthfirst', 
        'roots': roots
    }
    
    # Creating new stylesheet with white selected node
    new_cytoscape_stylesheet = cytoscape_stylesheet.copy()

    # Add styling for 
    if ind is not None: 
        new_cytoscape_stylesheet.append({
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
        
        new_cytoscape_stylesheet.append({
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

        new_cytoscape_stylesheet.append({
            'selector': f'[id = "{source}"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#000000',
            }
        }) 
        
        new_cytoscape_stylesheet.append({
            'selector': f'[id = "{target}"]',
            'style': {
                'background-color': '#FFFFFF',
                'border-color': '#6173E9',
                'border-width': '3px',
                'content': 'data(label)',
                'color': '#000000',
            }
        }) 
    
    return elements, cytoscape_layout, new_cytoscape_stylesheet


@callback( Output("individual-heading", "children"),  Output("individual-exceptions", "children"), Output("individual-genes", "children"), Output("individual-results", "children"), Input("cytoscape-family-tree", "tapNodeData"), Input("ind-select", "value"), Input("gen-select", "value"))
def set_values(ind_clicked, ind_select, gen_select):
    
    # Individual information
    ind = None
    gen = None
    extinct = None
    
    if ind_clicked is None: 
        
        # Get informatuon from selects
        ind = ind_select
        gen = gen_select.split('_')[1]
        extinct = False
    
    else:
        
        # Get informatuon from node
        ind = ind_clicked["id"]
        gen = ind_clicked["generation"]
        extinct = ind_clicked["extinct"]
    
    meas_keys = list(meas_info.keys())
    ind_meas = get_individual_result(run, gen, ind)
    ind_genome = get_individual_chromosome(run, gen, ind)
    
    # Creating heading div
    ind_heading = [html.H2(ind, style = {'margin': '10px'})]
    
    # Creating exceptions div
    ind_exceptions = []
    
    #if extinct:
    #    ind_exceptions += [information("Individual became extinct.")]
        
    #if "energy_consumption" in ind_meas and "inference_time" in ind_meas:
    #    if (type(ind_meas["energy_consumption"]) != int and type(ind_meas["energy_consumption"]) != float) or (type(ind_meas["inference_time"]) != int and type(ind_meas["inference_time"]) != float):            
    #        return ind_heading, warning("Measuring energy consumption failed with this individual"), [], []
    #else: 
    #    return ind_heading, warning("Measuring energy consumption failed with this individual"), [], []
    
    # Creating genes values
    ind_genes = [dot_heading("Genome", style={"margin": "10px",'flex': '100%'}), genome_overview(chromosome=ind_genome)]
    
    # Metric cards for objectives
    ind_fitness = [dot_heading("Fitness", style={"margin": "10px",'flex': '100%'})]
    
    if "fitness" in ind_meas:
        ind_fitness += [bullet_chart_basic(ind_meas['fitness'], 0, 3, metric_card_id="bullet-chart-basic")]

    for meas_key in meas_keys:
        if meas_key in ind_meas:
            
            #print(meas_key, ": ", meas_info[meas_key]["displayname"], " | ", meas_info[meas_key]["individual-info-img"], " | ", ind_meas[meas_key], " | ", border_meas[meas_key]['min']['value'], " | ", border_meas[meas_key]['max']['value'],  " | ")
            
            # TODO check whether keys in config
            ind_fitness += [(
                bullet_chart_card(
                    meas_info[meas_key]["displayname"], 
                    meas_info[meas_key]["individual-info-img"], 
                    ind_meas[meas_key], 
                    border_meas[meas_key][0], 
                    border_meas[meas_key][1], 
                    unit=meas_info[meas_key]["unit"], 
                    constraint=None, 
                    metric_card_id="bullet-chart-card"
                )
            )]
            
    
    return ind_heading, ind_exceptions, ind_genes, ind_fitness


### LAYOUT ###

layout = dmc.Grid(
    children=[
        
        ### FAMILY TREE ###
        dmc.Col(html.Div(
            [ 
                html.H1('Family Tree', style = {"margin-bottom": "20px", "margin-top": "20px"}), 
                node_select, 
                cytoscape,
                slider
            ]), 
            span='auto',
            style={'max-width': '100%'} # 100% needed for scaling cytoscape to 100%
        ),
        
        ### INDIVIDUAL INFORMATION ###
        dmc.Col([
            html.Div([], id='individual-heading'), 
            html.Div([], id='individual-exceptions'), 
            dmc.Grid(
                [
                    dmc.Col([html.Div([], id='individual-results')], span=10),
                    dmc.Col([html.Div([], id='individual-genes')], span='auto')
                ],
                gutter="xs",
                grow=True
            )], 
            span=4, 
            className='cytoscape-values', 
            id='values-col'),
    ],
    gutter="s",
    #justify='',
    grow=True
)
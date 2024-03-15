import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np
from dotenv import load_dotenv
import os
from alphashape import alphashape
from components import dot_heading, bullet_chart_card_basic, parameter_card, chromosome_sequence
from evolution import get_individuals, get_generations, get_meas_info, get_healthy_individuals_results, get_best_individuals
from genepool import get_unique_gene_colors

load_dotenv()
run = os.getenv("RUN_RESULTS_PATH")

dash.register_page(__name__, path='/results')


### GLOBAL VARIABLES
grid_gutter = 'xl'
fitn_obj_height = 180
healthy, unhealthy = get_healthy_individuals_results(run, as_generation_dict=False)
tot_gen = len(get_generations(run))
processed_gen = len(get_generations(run))
best_individuals = get_best_individuals(run)
unique_genes = get_unique_gene_colors(run)
measurements = get_meas_info(run)

### HELPER FUNCTIONS FOR PLOTS ###

def add_meas_trace(fig, run, meas, generation_range=None, min=None, max=None, show_std=True, linecolor='#6173E9'):
    
    # Defining borders to exclude and include invalid values
    if min is None:
        min = -100000000000
    if max is None:
        max = 100000000000

    # Get the indivuals' information by sotring the valid values in arrays
    gen_results = get_individuals(run, generation_range, value='results', as_generation_dict=True)
    
    generations = []
    avg_results = []
    std_results = []
    
    for gen, results in gen_results.items():
        
        values = []
        
        for ind, result in results.items():
            
            # TODO Why result None
            if result is not None and meas in result:
                value = result[meas]

                if (type(value) == int or type(value) == float) and (value <= max) and (value >= min): 
                    values.append(value)
            
        generations.append(gen)
        avg_results.append(np.mean(np.array(values)))
        std_results.append(np.std(np.array(values)))
    
    avg_results = np.array(avg_results)
    std_results = np.array(std_results)
    
    # Add standard deviation in background
    std_top = avg_results - std_results
    std_bottom = (avg_results + std_results)[::-1]
    
    if show_std:
        fig.add_trace(go.Scatter(
            x=np.concatenate([generations, generations[::-1]]),
            y=np.concatenate([std_top, std_bottom]),
            fill='toself',
            fillcolor='rgba(239,239,239,0.5)',
            line={'color':'rgba(239,239,239,0.5)'},
            name='Standard Deviation',
            hoverinfo='x+y'
        ))
    
    fig.add_trace(go.Scatter(
        x=generations,
        y=avg_results,
        mode='lines',
        name=measurements[meas]["displayname"],
        line=go.scatter.Line(color=linecolor),
        hoverinfo='x+y'
    ))     

def add_constraint_trace(fig, constraint):
    
    generations = get_generations(run, as_int=True)
    fig.add_trace(
        go.Scatter(
            x=generations, 
            y=[constraint] * len(generations), 
            name='Constraint',
            mode='lines', 
            line=go.scatter.Line(color='#B70202')
        )
    )

def figure_meas_over_gen(run, measures, generation_range=None, min=None, max=None, show_std=True, show_constraint=True, title=None, xaxis_title=None, yaxis_title=None):

    # Check if measures is a list or a string
    if type(measures) is str:
        measures = [measures]
    
    # Don't show standard deviation if more than one measure
    showlegend = False
    
    if len(measures) > 1:
        show_std=False
        show_constraint=False
        showlegend=True
        
    # Create figure
    fig = go.Figure()
    
    # Empty figure with no measures
    if len(measures) == 0:
        
        gens = list(range(1, 26))
        fig = go.Figure(go.Scatter(x=gens, mode='markers', marker=dict(color='rgba(0,0,0,0)')))
    
    # Measure traces
    else:   
        opacity_step = 1 / len(measures)
        for idx, meas in enumerate(measures):
        
            opacity = 1 - idx * opacity_step
            linecolor = f'rgba(97,115,233,{opacity})'
        
            add_meas_trace(fig, run, meas, generation_range, min, max, show_std, linecolor)
    
            # Constraint trace
            #if show_constraint:
            #    constraint = get_meas_info(run)[meas][1]
                
                #if constraint != None:
                #    add_constraint_trace(fig, constraint)
    
    # Layout
    t = 10 if title is None else 50
    
    fig.update_layout(
        title=title,
        title_font_color='#717171',
        title_font_size=15,
        title_font=dict(family='sans-serif'),
        xaxis={'title': xaxis_title, 'tickfont':{'color': '#D0D0D0'}, 'showline':True},
        yaxis={'title': yaxis_title, 'showgrid':True, 'gridcolor':'#D0D0D0', 'tickfont':{'color': '#D0D0D0'}},
        margin={'l': 10, 'b': 10, 't': t, 'r': 10},
        showlegend=showlegend,
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x",
    )
    
    return fig

def graph_meas_over_gen(run, measures, generation_range=None, min=None, max=None, show_std=True, max_width=430, height=200, width=None, show_constraint=True, title=None, xaxis_title=None, yaxis_title=None, id="graph-meas-over-gen"):
    
    fig = figure_meas_over_gen(run, measures, generation_range, min, max, show_std, show_constraint, title, xaxis_title, yaxis_title)
    
    graph_div = dcc.Graph(
        figure=fig, 
        style={'height': height, 'max-width': max_width, 'min-width': 200, 'width': width},
        id=id
    )
    
    return graph_div

def get_pareto_optimality_fig(run, generation_range=None, max_width=430, height=200):
    
    # Font of axis
    tickfont = {
        'color': '#D0D0D0', 
        'family': 'sans-serif',
    }
    
    titlefont = {
        'family': 'sans-serif', 
        'color': '#D0D0D0',     
        'size': 12,            
    }
        
    # Get all fitness objectives
    fitness_objectives = []
    
    for measurement, rules in measurements.items():
        if rules["pareto-optimlity-plot"]:
            fitness_objectives.append(measurement)
      
    numb_fo = len(fitness_objectives)
    obj1, obj2, obj3 = None, None, None
    marker = None
    
    # Special Cases
    if numb_fo == 0 or numb_fo == 1:
        return None
    elif numb_fo > 3:
        fitness_objectives = fitness_objectives[:3]
    
    # Objectives
    results, _ = get_healthy_individuals_results(run, as_generation_dict=False)
    
    if numb_fo == 2:
        obj1 = [result[fitness_objectives[0]] for result in results]
        obj2 = [result[fitness_objectives[1]] for result in results]
        
    elif numb_fo == 3:
        obj1 = [result[fitness_objectives[0]] for result in results]
        obj2 = [result[fitness_objectives[1]] for result in results]
        obj3 = [result[fitness_objectives[2]] for result in results]
        
        custom_colorscale = [
            [0.0, '#ACB5ED'], 
            [0.2, '#7D8CEF'], 
            [0.4, '#5666CD'], 
            [0.6, '#293AAA'], 
            [0.8, '#001075'], 
            [1.0, '#000B51']  
        ] 
        
        marker = dict(
            size=3,
            color=obj3,
            colorscale=custom_colorscale,
            reversescale=False,
            symbol='x',
            colorbar={
                'title':f"{measurements[fitness_objectives[2]]['displayname']} [{measurements[fitness_objectives[2]]['unit']}]",
                'thickness': 10,
                'tickfont': tickfont,
                'titlefont': titlefont,
                #'title_standoff': 20,
                #'title_textangle': -90,
                'orientation': 'h',
                'outlinecolor': '#D0D0D0'
            }
        )
    
    # Add pareto optimality scatter plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=obj1,
        y=obj2,
        mode='markers',
        marker=marker
    ))
    
    # Alpha Shape
    #points = list(zip(obj1, obj2))
    #alpha_shape = alphashape(points, 0.01)
    ##alpha_shape_vertices = np.array(alpha_shape.exterior.coords)
    #print(alpha_shape_vertices)
    
    #fig.add_trace(go.Scatter(
    #    x=alpha_shape_vertices[:, 0],
    #    y=alpha_shape_vertices[:, 1],
    #    mode='lines',
    #    line=dict(color='blue')
    ##))
    
    # Update layout of figure
    fig.update_layout(
        title="", # Pareto optimality
        title_font_color='#717171',
        title_font_size=15,
        title_font=dict(family='sans-serif'),
        xaxis={'title': f"{measurements[fitness_objectives[0]]['displayname']} [{measurements[fitness_objectives[0]]['unit']}]", 'showline':True , 'tickfont': tickfont, 'title_font': titlefont},
        yaxis={'title': f"{measurements[fitness_objectives[1]]['displayname']} [{measurements[fitness_objectives[1]]['unit']}]", 'showgrid':True, 'gridcolor':'#D0D0D0', 'tickfont': tickfont, 'title_font': titlefont},
        coloraxis=dict(
            colorbar=dict(
                tickfont=tickfont,  # Adjust tick font color and size
                titlefont=titlefont,  # Adjust title font color and size
                thickness=15  # Adjust thickness of the color axis
            )
        ),
        margin={'l': 10, 'b': 0, 't': 0, 'r': 10},
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x",
    )
    
    # Add plot to a dash component
    graph_div = dcc.Graph(
        figure=fig, 
        style={'height': height, 'max-width': max_width},
    )
    
    return graph_div


### GENERAL RUN OVERVIEW ###

def general_overview():
    gen_processed = bullet_chart_card_basic(processed_gen, 1, tot_gen, unit='Generations processed', info='Generations', back_color='#6173E9', bar_color='#A4B0FE', load_color='#FFFFFF', margin='0px', min_width='260px', flex='1')
    ind_healthy = parameter_card("Healthy Individuals", len(healthy), icon='icon-park-outline:health', margin='0px', width='100%')
    ind_unhealthy = parameter_card("Unhealthy Individuals", len(unhealthy), icon='mdi:robot-dead-outline', margin='0px', width='100%')
    fitness_plot = graph_meas_over_gen(run, 'fitness', generation_range=None, min=0, max=1, height=222.5, title="Fitness over generations", xaxis_title="", yaxis_title="")
    pareto_optimality_plot = get_pareto_optimality_fig(run, height=222.5)

    general_overview = dmc.Grid(
        [
            dmc.Col(dmc.Stack([gen_processed, ind_healthy, ind_unhealthy]), span='auto'),
            dmc.Col(fitness_plot, span=3, className="col-results-page"), 
            dmc.Col(pareto_optimality_plot, span=5, className="col-results-page"),
        ],
        gutter=grid_gutter,
        grow=True,
        justify='flex-start',
        className='general-overview'
    )
    
    return general_overview


### MEMORY PLOT ###
def memory_plot():
    mem_chips = dmc.ChipGroup(
        [
            dmc.Chip(
                x,
                value=x,
                variant="filled",
                color="indigo",
                size='xs',
            )
            for x in ["H5", "TFLite", "C Array"]
        ],
        id="mem-chips",
        value=["H5", "TFLite", "C Array"],
        multiple=True,
        style={'padding': '5px'}
    )
    
    memory = dmc.Col(
        [
            dot_heading('Memory', className='dot-heading-results-page', style={'width': '100px'}),     
            graph_meas_over_gen(run, ['memory_footprint_h5', 'memory_footprint_tflite', 'memory_footprint_c_array'], height=fitn_obj_height, id="mem-graph"),
            mem_chips
        ], 
        className="col-results-page"
    )
    
    return memory

#@callback(
#    Output("mem-graph", "figure"),
#    Input("mem-chips", "value"),
#)
def chips_values(mems):
    
    mems_key = {
        "H5": "memory_footprint_h5", 
        "TFLite": "memory_footprint_tflite", 
        "C Array": "memory_footprint_c_array",
    }
    
    return figure_meas_over_gen(run, [mems_key[mem] for mem in mems])


### INDIVIDUAL RUN RESULTS PLOT ###

def objectives_overview():
    
    objective_trends = []
    
    for measurement, meas_info in measurements.items():
        if meas_info.get("run-result-plot", True):
            
            heading = meas_info.get("displayname", measurement)
            
            if meas_info.get("unit", None):
                heading += f" [{meas_info.get('unit')}]"
            
            objective_trends.append(
                dmc.Col(
                    [
                        dot_heading(heading, style={"font-size": "14px"}, className='dot-heading-results-page'), 
                        graph_meas_over_gen(run, measurement, generation_range=None, min=meas_info.get("min-boundary", None), max=meas_info.get("max-boundary", None), height=fitn_obj_height, width=950)
                    ], 
                    className="col-results-page"
                )
            )
        
    objectives_overview = dmc.Grid(
        objective_trends,
        gutter=grid_gutter,
        grow=True,
        justify='flex-start'
    )
    
    return objectives_overview


### BEST INDIVIDUALS PLOT ###

def best_individuals_overview():
    
    genomes = []
    
    for gen, ind in best_individuals.items():
        
        # TODO WHYY
        if ind["individual"] is None:
            continue
        
        splits = ind["individual"].split("_")
        
        ind_abbrev = ""
        for split in splits:
            ind_abbrev += split[0].upper()
        
        ind_results = ind.copy()
        del ind_results["chromosome"]
        ind_results = str(ind_results)
        ind_results = ind_results.replace('{', '').replace('}', '').replace("'", '')
        
        ind_overview = html.Div(
            [
                dmc.Tooltip(
                    label=ind_results,
                    position="right",
                    offset=3,
                    transition="slide-up",
                    color='gray',
                    multiline=True,
                    width="300px",
                    children=[dmc.Avatar(ind_abbrev, radius="xl", style={"color": "#000000", "background-color": "#FFFFFF", "margin": "5px"})]
                ),
                html.P(f"GEN {gen}", style={"margin": "5px", "font-weight": "bold", "font-size": "11px"}),
                
                chromosome_sequence(ind["chromosome"], justify="flex-start", align="center", compromised=True, unique_genes=unique_genes),
            ],
            className="best-individual"
        )
        genomes.append(ind_overview)

    genomes_div = dmc.Group(genomes, position='apart', align='start', style={"gap":"5px"})
    
    return genomes_div


### PAGE LAYOUT ###

def performance_plots_div():
    return html.Div(
        children=[
            html.H1("Run Result Plots", style={'margin-bottom': '25px', 'margin-top': '25px'}),
            general_overview(),
            objectives_overview(),
        ]
    )

def best_individuals_div():
    return html.Div(
        children=[
            html.H1("Fittest Individuals", style={'margin-bottom': '25px', 'margin-top': '25px'}),
            best_individuals_overview()
        ]
    )

def run_results_layout():
    return dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Run results plots", value="plots"),
                dmc.Tab("Fittest individuals", value="best-individuals"),
            ]
        ),
        dmc.TabsPanel(performance_plots_div(), value="plots"),
        dmc.TabsPanel(best_individuals_div(), value="best-individuals"),
    ],
    color="indigo",
    orientation="horizontal",
    variant="default",
    value="plots"
)

layout = run_results_layout
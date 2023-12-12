import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np
from alphashape import alphashape
from components import dot_heading, bullet_chart_basic, metric_card, genome_overview
from utils import get_individuals, get_generations, get_meas_info, get_hyperparamters, get_healthy_individuals_results, get_best_individuals

dash.register_page(__name__, path='/results')


### GLOBAL VARIABLES
run = 'ga_20230116-110958_sc_2d_4classes'

grid_gutter = 'xl'
fitn_obj_height = 150

healthy, unhealthy = get_healthy_individuals_results(run, as_generation_dict=False)
tot_gen = get_hyperparamters(run)['generations']
processed_gen = len(get_generations(run))

best_individuals = get_best_individuals(run)


### HELPER FUNCTIONS FOR PLOTS ###
# TODO Exclude all unhealthy individuals

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
            
            if meas in result:
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
    
    # Add mean in foreground
    names = {
        'memory_footprint_h5': 'H5',
        'memory_footprint_c_array': 'C Array',
        'memory_footprint_tflite': 'TFLite',
        'val_acc': 'Accuracy',
        'fitness': 'Fitness',
        'inference_time': 'Inference time',
        'energy_consumption': 'Energy consumption',
        'mean_power_consumption': 'Mean power consumption'
    }
    
    fig.add_trace(go.Scatter(
        x=generations,
        y=avg_results,
        mode='lines',
        name=names[meas],
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
            if show_constraint:
                constraint = get_meas_info(run)[meas][1]
                
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

def graph_meas_over_gen(run, measures, generation_range=None, min=None, max=None, show_std=True, max_width=430, height=200, show_constraint=True, title=None, xaxis_title=None, yaxis_title=None, id="graph-meas-over-gen"):
    
    fig = figure_meas_over_gen(run, measures, generation_range, min, max, show_std, show_constraint, title, xaxis_title, yaxis_title)
    
    graph_div = dcc.Graph(
        figure=fig, 
        style={'height': height, 'max-width': max_width},
        id=id
    )
    
    return graph_div

def get_pareto_optimality_fig(run, generation_range=None, max_width=430, height=200):
    
    # TODO Alpha shape
    
    # Get the results of all healthy individuals
    results, _ = get_healthy_individuals_results(run, as_generation_dict=False)
    
    mems = [result["memory_footprint_tflite"] for result in results]
    enes = [result["energy_consumption"] for result in results]
    vals = [result["val_acc"] for result in results]
    
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
    
    # Add pareto optimality scatter plot
    fig = go.Figure()
    
    custom_colorscale = [
        [0.0, '#000B51'], 
        [0.2, '#001075'], 
        [0.4, '#293AAA'], 
        [0.6, '#5666CD'], 
        [0.8, '#7D8CEF'], 
        [1.0, '#ACB5ED']  
    ]   

    fig.add_trace(go.Scatter(
        x=mems,
        y=enes,
        mode='markers',
        marker=dict(
            size=3,
            color=vals,
            colorscale=custom_colorscale,
            reversescale=False,
            symbol='x',
            colorbar={
                'title':'Validation \nAccuracy',
                'thickness': 10,
                'tickfont': tickfont,
                'titlefont': titlefont,
                #'title_standoff': 20,
                #'title_textangle': -90,
                'orientation': 'h',
                'outlinecolor': '#D0D0D0'
            }
        )
    ))
    
    # Update layout of figure
    fig.update_layout(
        title="Pareto optimality",
        title_font_color='#717171',
        title_font_size=15,
        title_font=dict(family='sans-serif'),
        xaxis={'title': "Memory footprint TFLite (B)", 'showline':True , 'tickfont': tickfont, 'title_font': titlefont},
        yaxis={'title': "Energy Consumption (mJ)", 'showgrid':True, 'gridcolor':'#D0D0D0', 'tickfont': tickfont, 'title_font': titlefont},
        coloraxis=dict(
            colorbar=dict(
                tickfont=tickfont,  # Adjust tick font color and size
                titlefont=titlefont,  # Adjust title font color and size
                thickness=15  # Adjust thickness of the color axis
            )
        ),
        margin={'l': 10, 'b': 0, 't': 100, 'r': 10},
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x",
        yaxis_range=[1, 6],  
        xaxis_range=[10000, 60000],  
    )
    
    # Add plot to a dash component
    graph_div = dcc.Graph(
        figure=fig, 
        style={'height': height, 'max-width': max_width},
    )
    
    return graph_div


### GENERAL RUN OVERVIEW ###

def general_overview():
    gen_processed = bullet_chart_basic(processed_gen, 1, tot_gen, unit='Generations processed', info='Generations', back_color='#6173E9', bar_color='#A4B0FE', load_color='#FFFFFF', margin='0px', min_width='260px', flex='1')
    ind_healthy = metric_card("Healthy Individuals", len(healthy), icon='icon-park-outline:health', margin='0px', width='100%')
    ind_unhealthy = metric_card("Unhealthy Individuals", len(unhealthy), icon='mdi:robot-dead-outline', margin='0px', width='100%')
    fitness_plot = graph_meas_over_gen(run, 'fitness', generation_range=None, min=0, max=1, height=222.5, title="Fitness over generations", xaxis_title="", yaxis_title="")
    pareto_optimality_plot = get_pareto_optimality_fig(run, height=222.5)

    general_overview = dmc.Grid(
        [
            dmc.Col(dmc.Stack([gen_processed, ind_healthy, ind_unhealthy], ), span='auto'),
            dmc.Col(fitness_plot, span=5, className="col-results-page"), 
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

@callback(
    Output("mem-graph", "figure"),
    Input("mem-chips", "value"),
)
def chips_values(mems):
    
    mems_key = {
        "H5": "memory_footprint_h5", 
        "TFLite": "memory_footprint_tflite", 
        "C Array": "memory_footprint_c_array",
    }
    
    return figure_meas_over_gen(run, [mems_key[mem] for mem in mems])


### INDIVIDUAL RUN RESULTS PLOT ###

def objectives_overview():
    objectives_overview = dmc.Grid(
        [
            dmc.Col([dot_heading('Accuracy', className='dot-heading-results-page'), graph_meas_over_gen(run, 'val_acc', generation_range=None, min=0, max=1, height=fitn_obj_height)], className="col-results-page"), 
            memory_plot(),
            dmc.Col([dot_heading('Inference Times', className='dot-heading-results-page'), graph_meas_over_gen(run, 'inference_time', generation_range=None, height=fitn_obj_height)], className="col-results-page"), 
            dmc.Col([dot_heading('Mean Power Consumption', className='dot-heading-results-page'), graph_meas_over_gen(run, 'mean_power_consumption', generation_range=None, height=fitn_obj_height)], className="col-results-page"), 
            dmc.Col([dot_heading('Power Measurement', className='dot-heading-results-page'), graph_meas_over_gen(run, 'energy_consumption', generation_range=None, height=fitn_obj_height)], className="col-results-page")     
        ], 
        gutter=grid_gutter,
        grow=True,
        justify='flex-start'
    )
    
    return objectives_overview


### BEST INDIVIDUALS PLOT ###

def best_individuals_overview():
    
    genomes = []
    
    for gen, ind in best_individuals.items():
        
        ind_overview = html.Div(
            [
                #html.P(gen, style={"margin": "5px", "font-weight": "lighter","font-size": "15px", "width":"200px"}),
                #html.H4(ind["individual"].replace("_", "\n"), style={ "margin": "5px" }),
                genome_overview(ind["chromosome"], justify="flex-start", align="center"),
            ],
            className="best-individual"
        )
        genomes.append(ind_overview)

    genomes_div = dmc.Group(genomes, align='start')
    
    return genomes_div

### PAGE LAYOUT ###

plots_div = html.Div(
    children=[
        html.H1("Run Result Plots", style={'margin-bottom': '25px', 'margin-top': '25px'}),
        general_overview(),
        objectives_overview(),
    ]
)

best_individuals_div = html.Div(
    children=[
        html.H1("Best Individuals", style={'margin-bottom': '25px', 'margin-top': '25px'}),
        best_individuals_overview()
    ]
)

layout = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Run results plots", value="plots"),
                dmc.Tab("Best individuals", value="best-individuals"),
            ]
        ),
        dmc.TabsPanel(plots_div, value="plots"),
        dmc.TabsPanel(best_individuals_div, value="best-individuals"),
    ],
    color="indigo",
    orientation="horizontal",
    variant="default",
    value="plots"
)
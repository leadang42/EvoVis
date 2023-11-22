import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/results')

from components import dot_heading
from utils import get_individuals

run = 'ga_20230116-110958_sc_2d_4classes'

def get_result_over_gen_fig(run, meas, generation_range=None, min=None, max=None):
    """_summary_

    Args:
        run (str): The directory name of the run data.
        meas (str): _description_
        generation_range (range): A python range of generations from which the individuals will be extracted. Defaults to None.
        min (float, optional): . Defaults to None.
        max (float, optional): . Defaults to None.
    """
    if min is None:
        min = -100000000000
    if max is None:
        max = 100000000000
        
    gen_results = get_individuals(run, generation_range=None, value='results', as_generation_dict=True)
    
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
    
    # Mean
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=generations,
        y=avg_results,
        mode='lines',
        name='Mean',
        line=go.scatter.Line(color='#6173E9'),
        hoverinfo='x+y'
    ))
 
    # Standard deviation
    fig.add_trace(go.Scatter(
        x=np.concatenate([generations, generations[::-1]]),
        y=np.concatenate([avg_results - std_results, (avg_results + std_results)[::-1]]),
        fill='toself',
        fillcolor='rgba(239,239,239,0.5)',
        line={'color':'rgba(239,239,239,0.5)'},
        name='Standard Deviation',
        hoverinfo='none'
    ))

    # Layout
    fig.update_layout(
        title=None,
        xaxis={'title': 'Generations', 'tickfont':{'color': '#D0D0D0'}, 'showline':True},
        yaxis={'title': None, 'showgrid':True, 'gridcolor':'#D0D0D0', 'tickfont':{'color': '#D0D0D0'}},
        margin={'l': 10, 'b': 10, 't': 10, 'r': 10},
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    graph_div =  dcc.Graph(
        id='line-plot',
        figure=fig, 
        style={'height': 200}
    )
    
    return graph_div


grid_gutter = 'xl'

layout = html.Div(
    children=[
        html.H1("Results", style={'margin-bottom': '50px', 'margin-top': '30px'}),
        dmc.Grid(),
        dmc.Grid([
            dmc.Col([dot_heading('Fitness'), get_result_over_gen_fig(run, 'fitness', generation_range=None, min=0, max=1)], span=6), 
            dmc.Col([dot_heading('Pareto Optimality')], span=6)], 
            gutter=grid_gutter
        ),
        dmc.Grid([
            dmc.Col([dot_heading('Accuracy'), get_result_over_gen_fig(run, 'val_acc', generation_range=None, min=0, max=1)], span=4), 
            dmc.Col([dot_heading('Memory'), get_result_over_gen_fig(run, 'memory_footprint_h5', generation_range=None)], span=4), 
            dmc.Col([dot_heading('Inference Times'), get_result_over_gen_fig(run, 'inference_time', generation_range=None)], span=4)], 
            gutter=grid_gutter
        ),
    ]
)

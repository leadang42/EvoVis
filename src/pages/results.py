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


def get_pareto_optimality_fig(run, meas, generation_range=None, min=None, max=None):
    fig = go.Figure()
    
    x_data = None
    y_data = None
    z_data = None
    color_data = None
    timestamps = None
    
    scatter = go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='markers',
        marker=dict(
            size=8,
            color=color_data,
            colorscale='Viridis',
            opacity=0.8
        )
    )

    fig.add_trace(scatter)

    # Add slider for animation
    fig.update_layout(
        sliders=[{
            "steps": [
                {"args": [[f'{hour:02d}' for hour in range(int(timestamp), int(timestamp)+1)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}}],
                "label": f"{int(timestamp)} hours",
                "method": "animate"} for timestamp in timestamps
            ],
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 12},
                "prefix": "Timestamp:",
                "visible": True,
                "xanchor": "right",
                "yanchor": "top"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"}
        }],
        updatemenus=[{
            "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                "label": "Play",
                "method": "animate",
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate",
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top",
        }]
    )

    # Customize layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X-axis'),
            yaxis=dict(title='Y-axis'),
            zaxis=dict(title='Z-axis')
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        scene_aspectmode='cube'
    )
    
grid_gutter = 'xl'

layout = html.Div(
    children=[
        html.H1("Results", style={'margin-bottom': '50px', 'margin-top': '30px'}),
        dmc.Grid(),
        dmc.Grid([
            dmc.Col([dot_heading('Fitness', className='dot-heading-results-page'), get_result_over_gen_fig(run, 'fitness', generation_range=None, min=0, max=1)], span=6), 
            dmc.Col([dot_heading('Pareto Optimality', className='dot-heading-results-page')], span=6)],
            gutter=grid_gutter
        ),
        dmc.Grid([
            dmc.Col([dot_heading('Accuracy', className='dot-heading-results-page'), get_result_over_gen_fig(run, 'val_acc', generation_range=None, min=0, max=1)], span=4), 
            dmc.Col([dot_heading('Memory', className='dot-heading-results-page'), get_result_over_gen_fig(run, 'memory_footprint_h5', generation_range=None)], span=4), 
            dmc.Col([dot_heading('Inference Times', className='dot-heading-results-page'), get_result_over_gen_fig(run, 'inference_time', generation_range=None)], span=4)], 
            gutter=grid_gutter
        ),
    ]
)

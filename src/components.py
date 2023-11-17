import dash
from dash import html, dcc
from dash_iconify import DashIconify
import plotly.graph_objects as go

app = dash.Dash(__name__)

def dot_heading(heading, style=None):
    heading_div = html.Div(
        [
            DashIconify(icon="material-symbols:circle", height=12, width=12, color="#6173E9", 
                style={ 
                    "display": "inline-block", 
                    "vertical-align":"center" 
                }),
            html.H4(heading, 
                style={ 
                    "display": "inline-block",
                    "margin": "5px", 
                    "vertical-align":"center" 
                })
        ],
        className="dot-heading",
        style=style
    )
    return heading_div


def metric_card(metrictype, metric, icon, width="260px", metric_card_id="metric-card"):
    metric_card_style = {
        'width': width,
        'display': 'inline-flex',
        'margin': '5px',
        'vertical-align': 'center',
        'background-color': '#FFFFFF',
        'border-radius': '20px',
        'align-items': 'center',
        'justify-content': 'flex-start',
        'box-shadow': '3px 3px 10px 1px rgba(0, 0, 0, 0.05)',
    }

    text_block_style = {
        "margin": "5px", 
        "vertical-align":"center",
        "background-color": "#FFFFFF",
    }

    metric_card_div = html.Div([

        html.Button(children=DashIconify(icon=icon, height=25, width=25, color="#000000"), className="metric-btn"),

        html.Div([   
            html.P(metrictype, style={"margin": "5px", "font-weight": "lighter","font-size": "15px",}, id=f"{metric_card_id}-label"),
            html.H4(metric, style={ "margin": "5px" }, id=f"{metric_card_id}-value")],
            style= text_block_style)   
        ], 
        
        style = metric_card_style, 
        id = metric_card_id
    )

    return metric_card_div


def bullet_chart_card(metrictype, img, metric, min, max, constraint=None, unit=None, min_width='200px', metric_card_id="bullet-chart-card"):
    
    metric = round(metric, 3)
    
    bullet_chart_card_style = {
        'border-radius': '20px',
        'border': '3px solid #FFFFFF',
        'background': '#EFEFEF',
        'min-width': min_width,
        'margin': '10px',
        'margin-top': '30px',
        'flex-grow': '1',
        
        'position': 'relative',
        'display': 'inline-flex',
        'justify-content': 'center',
    }
    
    bullet_chart_style = {
        'border-radius': '15px',
        'border': '1px solid #FFFFFF',
        'background': 'linear-gradient(180deg, rgba(217, 217, 217, 0) 0%, rgba(97, 115, 233, 0.40) 178.92%)',
        'backdrop-filter': 'blur(3px)',
        'width': '95%',
        'height': '50%',
        'margin': '3px',
        'margin-top': '20px',
        'text-align': 'center',
        'z-index': 0,
    }
    
    img_style = {
        'width': '70px',
        'height': '70px',
        'flex-shrink': 0,
        'top': '-30px',
        'position': 'absolute',
        'z-index': 1,
    }
    
    bar_style = {
        'border-radius': '30px',
        'background': '#FFFFFF',
        'position': 'relative',
        'height': 20,
        'margin': '5px',
    }
    
    range = max - min
    
    load_percent = ((metric - min) / range * 100) if range != 0 else 0
    
    load_style = {
        'border-radius': '30px',
        'background': '#6173E9',
        
        'position': 'absolute',
        'z-index': 0,
        'height': 20,
        'width': f'{load_percent}%',
        
    }
    
    constraint_style = None
    if constraint is not None:
        constraint_percent = ((constraint - min) / range * 100) if range != 0 else 0
        if constraint_percent > 100: constraint_percent = 100
        if constraint_percent < 0: constraint_percent = 0

        constraint_style = {
            'background': '#B70202',
            'border-radius': '3px',
        
            'position': 'absolute',
            'z-index': 1,
            'height': 20,
            'width': 3,
            'left': f'{constraint_percent}%',
        }
    
    fig = go.Figure(go.Indicator(
        mode = "number+gauge+delta",
        gauge={
            'shape': "bullet",
            'axis': {'visible': False},
            'bar': {'color': "lightblue", 'line': {'color': "darkblue", 'width': 2}},
        },
        value = 220,
        delta = {'reference': 300},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': ""})
    )
    
    fig.update_layout(
        yaxis={'visible': False},
        yaxis_title_text='',
        yaxis_showgrid=False,
        yaxis_zeroline=False,
        yaxis_showticklabels=False,
        xaxis={'visible': False},
        xaxis_title_text='',
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        xaxis_showticklabels=False,
        height = 50,
        margin=dict(t=5, b=5, l=5, r=5),
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    
    metric_str = f'{metric} {unit}' if unit is not None else str(metric)
    
    bullet_chart_card_div = html.Div(
        [
            html.Img(src=f"assets/media/{img}.png", style=img_style, id=img),
            html.Div(
                [
                    html.P(metrictype, style={"margin": "5px", "margin-top": "20px", "font-weight": "lighter", "font-size": "15px", 'white-space': 'nowrap'}, id=f"{metric_card_id}-label"),
                    html.H4(metric_str, style={ "margin": "5px" , 'white-space': 'nowrap'}, id=f"{metric_card_id}-value"),
                    #dcc.Graph(figure=fig, className="bullet_chart"),
                    html.Div( [ html.Div([], style=load_style), html.Div([], style=constraint_style) ] ,style=bar_style)
                ],
                style = bullet_chart_style
            ),
            
        ],
        style = bullet_chart_card_style,
        id = metric_card_id
    )
    
    return bullet_chart_card_div


def bullet_chart_basic(metric, min, max, metric_card_id="bullet-chart-basic"):
    
    metric = round(metric, 3)
    range = max - min
    load_percent = ((metric - min) / range * 100) if range != 0 else 0
    
    bullet_chart_basic_style = {
        'border-radius': '20px',
        'background': '#FFFFFF',
        'padding': '10px',
        'margin': '10px',
        'display': 'block',
        'flex': '100%'
    }
    
    bar_style = {
        'border-radius': '30px',
        'background': '#EFEFEF',
        'position': 'relative',
        'height': 20,
    }
    
    load_style = {
        'border-radius': '30px',
        'background': '#6173E9',
        'height': 20,
        'width': f'{load_percent}%',
    }
    
    bullet_chart_basic_div = html.Div(
        [
            html.H4(str(metric), style={ "margin": "5px", 'width': '100%','white-space': 'nowrap'}, id=f"{metric_card_id}-value"),
            html.Div( [ html.Div([], style=load_style)], style=bar_style)
        ],
        style = bullet_chart_basic_style
    )
    
    return bullet_chart_basic_div
    

def warning(message):
    
    children = [DashIconify(icon='mingcute:information-line', height=25, width=25), html.P(message, className='feedback-text')]
    warning_div = html.Div(children=children, className="feedback feedback-warning")
    
    return warning_div


def information(message):
    
    children = [DashIconify(icon='mingcute:information-line', height=25, width=25), html.P(message, className='feedback-text')]
    warning_div = html.Div(children=children, className="feedback feedback-information")
    
    return warning_div


app.layout = html.Div([dot_heading("fitness"), metric_card("max memory footprint", "800000 B", "fluent:memory-16-regular")])

if __name__ == "__main__":
    app.run(debug=True)
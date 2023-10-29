import dash
from dash import html
from dash_iconify import DashIconify

app = dash.Dash(__name__)

def dot_heading(heading):
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


app.layout = html.Div([dot_heading("fitness"), metric_card("max memory footprint", "800000 B", "fluent:memory-16-regular")])

if __name__ == "__main__":
    app.run(debug=True)
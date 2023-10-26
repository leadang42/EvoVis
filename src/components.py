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

def metric_card(metrictype, metric, icon):
    metric_card_div = html.Div(
        [
            html.Button(children=DashIconify(icon=icon, height=25, width=25, color="#000000"), className="metric-btn"),
            html.Div(
                [   
                    html.P(
                        metrictype,
                        style={ 
                            "margin": "5px",
                            "font-weight": "lighter",
                            "font-size": "15px",
                        }),
                    html.H4(metric, 
                        style={ 
                            "margin": "5px"
                        })
                ],
                style={ 
                    "margin": "5px", 
                    "vertical-align":"center",
                    "background-color": "#FFFFFF",
                }
            )   
        ], 
        className="metric-card"
    )

    return metric_card_div

app.layout = html.Div([dot_heading("fitness"), metric_card("max memory footprint", "800000 B", "fluent:memory-16-regular")])

if __name__ == "__main__":
    app.run(debug=True)
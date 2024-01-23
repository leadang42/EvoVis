import dash
from dash import dcc, html, Input, Output, callback
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

app = dash.Dash(__name__, use_pages=True)

# Navigation bar with run select and navigation items
navbar = html.Div(
    [
        html.Div(
            [   
                html.A(children=html.Img(src="assets/media/evonas-logo.png", height="50px"), href=dash.page_registry['pages.hyperparameters']['relative_path']),
                
                # TODO Replace with just the pathname
                dmc.Select( label="Select run", placeholder="Select run", icon=DashIconify(icon="mdi:run", height=20, width=20, color="#6173E9"), data=["run"], id="run-select", className="circle-select-nav",),
            ],
            id="navrun"
        ),
        html.Div(
            [
                html.A(html.Button(children=DashIconify(icon="bi:github", height=25, width=25, color="#000000"), className="circle-btn", id="github-link"), href="https://github.com/leadang42/EvoNAS-Dashboard.git", target="_blank"),
                html.A(html.Button(children=DashIconify(icon="tabler:math-function", height=25, width=25, color="#000000"), className="circle-btn", id="hyperparameter-link"), href=dash.page_registry['pages.hyperparameters']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="tabler:dna", height=25, width=25, color="#000000"), className="circle-btn", id="genepool-link"), href=dash.page_registry['pages.genepool']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="grommet-icons:graph-ql", height=25, width=25, color="#000000"), className="circle-btn", id="family-tree-link"), href=dash.page_registry['pages.family_tree']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="simple-line-icons:graph", height=25, width=25,color="#000000"), className="circle-btn", id="results-link"), href=dash.page_registry['pages.results']['relative_path']),
                
            ],
            id="navlinks",
        )    
    ],
    id="navbar",
)

# Store run in callback
@callback(
    output=Output("run-value", "data"), 
    inputs=Input("run-select", "value")
)
def new_item(value):
    return value

# Pages from multipage
page = html.Div([ dash.page_container], id="page-content")

# Page Layout with navbar and pages from multipage
app.layout = html.Div([dcc.Location(id="url"), dcc.Store(id="run-value"), navbar, page])

if __name__ == "__main__":
    app.run()
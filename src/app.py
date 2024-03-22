import dash
from dash import html
from dash_iconify import DashIconify

### LAYOUT COMPONENTS
def navbar():
    return html.Div(
    [
        html.Div(
            [   
                html.A(children=html.Img(src="assets/media/evonas-logo.png", height="50px"), href=dash.page_registry['pages.hyperparameters_page']['relative_path']),
            ],
            id="navrun"
        ),
        html.Div(
            [
                html.A(html.Button(children=DashIconify(icon="streamline:input-box-solid", height=25, width=25, color="#000000"), className="circle-btn", id="hyperparameter-link"), href=dash.page_registry['pages.hyperparameters_page']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="jam:dna", height=25, width=25, color="#000000"), className="circle-btn", id="genepool-link"), href=dash.page_registry['pages.genepool_page']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="mdi:graph", height=25, width=25, color="#000000"), className="circle-btn", id="family-tree-link"), href=dash.page_registry['pages.family_tree_page']['relative_path']),
                html.A(html.Button(children=DashIconify(icon="entypo:bar-graph", height=25, width=25,color="#000000"), className="circle-btn", id="results-link"), href=dash.page_registry['pages.run_results_page']['relative_path']), 
            ],
            id="navlinks",
        )    
    ],
    id="navbar",
)

def page():
    return html.Div([ dash.page_container], id="page-content")

def app_layout():
    
    return html.Div([
        navbar(), 
        page()
    ])

### DASH APP & LAYOUT 
app = dash.Dash(__name__, use_pages=True)
app.layout = app_layout

if __name__ == "__main__":
    app.run(debug=True)
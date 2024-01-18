import dash
from dash import html, callback, Output, Input
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from components import dot_heading, metric_card
from utils import get_hyperparamters

dash.register_page(__name__, path='/')
run = "ga_20240108-231402_spoken_languages"     

### USED FILES FROM EVONAS RUN: config.json ### 

def grouped_metriccards(run):
    """Generates hyperparameter metric card divs that are assigned to their specified group divs.

    Args:
        run (str): Path where EvoNAS run configurations and results are stored.

    Returns:
        list: Hyperparameter groups, which display the group name as the header and the hyperparameter metric maps.
    """
    
    # Get the hyperparameters from file config.json
    hps = get_hyperparamters(run)
    
    # Store group key with list of metriccards
    groups = {}
    other_params = []

    for hp_key, hp in hps.items():
    
        # Extract values of hyperparameter and handle missing keys
        value = hp["value"] if "value" in hp else None
        display = hp["display"] if "display" in hp else True
    
        # Create a metriccard if hyperparam has a value and should be displayed
        if value is not None and display: 
            
            # Extract values of hyperparameter and handle missing keys
            unit = hp["unit"] if "unit" in hp else None
            icon = hp["icon"] if "icon" in hp else None
            displayname = hp["displayname"] if "displayname" in hp else None
            group = hp["group"] if "group" in hp else None
            description = hp["description"] if "description" in hp else None
            metrictype = displayname if displayname is not None else hp_key.replace("_", " ").capitalize()
            metric = str(hp["value"]).replace("\n", "")
            
            # Metric card div component for hyperparam visual
            mc = metric_card(metrictype=metrictype, metric=metric, icon=icon, unit=unit, description=description)
            
            # Add the metric card to its group
            if hp["group"] is None:
                other_params.append(mc)
                
            elif hp["group"] not in groups:
                groups[group] = [mc]
            
            else:
                groups[group].append(mc)

    # Add hyperparams without a group to the end
    if len(other_params) != 0:   
        groups["Other parameters"] = other_params
    
    # Convert the group dicts to list of divs  
    group_divs = []

    # Create group div with group heading and metriccards for each group
    for group_key, group in groups.items():   
        group_div = html.Div([dot_heading(group_key)] + group, className="metrics")
        group_divs.append(group_div)

    return group_divs

def parameter_overview_header():
    """Generate hyperparameter page header.

    Returns:
        list: Divs of header and cover image.
    """
    
    return [
        html.H1("Parameters"),
        html.H1("Overview"),
        html.Img(src="assets/media/evolution-cover.png", id="evolution-cover"),
    ]

layout = dmc.Grid(
    children=[
        dmc.Col(parameter_overview_header(), span='auto', className='hyperparameters-header'),
        dmc.Col(grouped_metriccards(run), span=8)
    ],
    justify="center",
    gutter="sm",
)

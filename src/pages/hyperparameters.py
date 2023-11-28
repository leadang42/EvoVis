import dash
from dash import html
import dash_mantine_components as dmc
from components import dot_heading, metric_card, fitness_function
from utils import get_hyperparamters

dash.register_page(__name__, path='/hyperparameters')

run = "ga_20230116-110958_sc_2d_4classes"

### Parameters Overview and gene image ###
header = dmc.Col(
    [
        html.H1("Parameters"),
        html.H1("Overview"),
        html.Img(src="assets/media/evolution-cover.png", id="evolution-cover"),
    ],
    span='auto',
    className='hyperparameters-header',
)

### Hyperparameters ###
evonas = html.Div(
    [
        dot_heading("Evonas parameters"),
        metric_card("Generations", get_hyperparamters(run)["generations"], "iconoir:tree"),
        metric_card("Population", get_hyperparamters(run)["population_size"], "pepicons-pencil:people"),
        metric_card("Best models crossover", get_hyperparamters(run)["nb_best_models_crossover"], "game-icons:podium-winner"),
        metric_card("Mutation rate", get_hyperparamters(run)["mutation_rate"], "ph:virus"),
        metric_card("Max feature layers", get_hyperparamters(run)["max_nb_feature_layers"], "cil:search"),
        metric_card("Max classification layers", get_hyperparamters(run)["max_nb_classification_layers"], "ph:tag"),
    ],
    className="metrics"
)

training = html.Div(
    [
        dot_heading("Training parameters"),
        metric_card("Input shape", str(get_hyperparamters(run)["input_shape"]), "uil:square-shape"),
        metric_card("Number of classes", get_hyperparamters(run)["nb_classes"], "octicon:number-24"),
        metric_card("Classes filter", str(get_hyperparamters(run)["classes_filter"]), "bi:collection-play"),
        metric_card("Number of epochs", get_hyperparamters(run)["nb_epochs"], "akar-icons:arrow-cycle"),
    ],
    className="metrics",
)

fitness = html.Div(
    [
        dot_heading("Fitness parameters"),
        fitness_function(),
        metric_card("Max memory footprint", f'{get_hyperparamters(run)["max_memory_footprint"]} B', "fluent:memory-16-regular"),
        metric_card("Max inference time", f'{get_hyperparamters(run)["max_inference_time"]} ms', "uiw:time-o"),
        metric_card("Max energy consumption", f'{get_hyperparamters(run)["max_energy_consumption"]} mJ', "simple-line-icons:energy"),
    ],
    className="metrics"
)

hyperparams = dmc.Col(
    [ 
        evonas,  
        fitness,  
        training
    ], 
    span=8
)

### Layout with Grid Layout ###
layout = dmc.Grid(
    children=[
        header,
        hyperparams,

    ],
    justify="center",
    gutter="sm",
)

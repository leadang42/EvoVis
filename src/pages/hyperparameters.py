import dash
from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from components import dot_heading, metric_card
from utils import generations, hyperparamters

dash.register_page(__name__, path='/hyperparameters')

run = "ga_20230116-110958_sc_2d_4classes"

evonas = html.Div(
    [
        dot_heading("Evonas parameters"),
        metric_card("Generations", hyperparamters(run)["generations"], "iconoir:tree"),
        metric_card("Population", hyperparamters(run)["population_size"], "pepicons-pencil:people"),
        metric_card("Best models crossover", hyperparamters(run)["nb_best_models_crossover"], "game-icons:podium-winner"),
        metric_card("Mutation rate", hyperparamters(run)["mutation_rate"], "ph:virus"),
        metric_card("Max feature layers", hyperparamters(run)["max_nb_feature_layers"], "cil:search"),
        metric_card("Max classification layers", hyperparamters(run)["max_nb_classification_layers"], "ph:tag"),
    ],
    className="wrapper"
)

training = html.Div(
    [
        dot_heading("Training parameters"),
        metric_card("Input shape", str(hyperparamters(run)["input_shape"]), "uil:square-shape"),
        metric_card("Number of classes", hyperparamters(run)["nb_classes"], "octicon:number-24"),
        metric_card("Classes filter", str(hyperparamters(run)["classes_filter"]), "bi:collection-play"),
        metric_card("Number of epochs", hyperparamters(run)["nb_epochs"], "akar-icons:arrow-cycle"),
    ],
    className="wrapper",
)

fitness = html.Div(
    [
        dot_heading("Fitness parameters"),
        metric_card("Max memory footprint", f'{hyperparamters(run)["max_memory_footprint"]} B', "fluent:memory-16-regular"),
        metric_card("Max inference time", f'{hyperparamters(run)["max_inference_time"]} ms', "uiw:time-o"),
        metric_card("Max energy consumption", f'{hyperparamters(run)["max_energy_consumption"]} mJ', "simple-line-icons:energy"),
    ],
    className="wrapper"
)

col1a = html.Div(
    [
        html.H1("Parameters"),
        html.H1("Overview"),
        html.Img(src="assets/media/evolution-cover.png", id="evolution-cover"),
    ],
    className="wrapper-col"
)

col1b = html.Div([evonas, fitness, training], className="wrapper-col", style={ "max-width": "850px" })

first_row = html.Div([ col1a, col1b ], className="wrapper")
#second_row = html.Div([ training ], className="wrapper")

layout = html.Div([ first_row ], className="wrapper")
import dash
from dash import html, dcc
import dash_latex as dl
import dash_mantine_components as dmc
from components import dot_heading, metric_card, fitness_function, fitnes_function_latex
from utils import get_hyperparamters

dash.register_page(__name__, path='/')

run = "ga_20230116-110958_sc_2d_4classes"
#run = "cifar10_diversity_06 2"

hyperparams = get_hyperparamters(run)

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
        metric_card("Generations", hyperparams["generations"], "iconoir:tree"),
        metric_card("Population", hyperparams["population_size"], "pepicons-pencil:people"),
        metric_card("Best models crossover", hyperparams["nb_best_models_crossover"], "game-icons:podium-winner"),
        metric_card("Mutation rate", hyperparams["mutation_rate"], "ph:virus"),
        metric_card("Max feature layers", hyperparams["max_nb_feature_layers"], "cil:search"),
        metric_card("Max classification layers", hyperparams["max_nb_classification_layers"], "ph:tag"),
    ],
    className="metrics"
)

training = html.Div(
    [
        dot_heading("Training parameters"),
        metric_card("Input shape", str(hyperparams["input_shape"]), "uil:square-shape"),
        metric_card("Number of classes", hyperparams["nb_classes"], "octicon:number-24"),
        metric_card("Classes filter", str(hyperparams["classes_filter"]), "bi:collection-play"),
        metric_card("Number of epochs", hyperparams["nb_epochs"], "akar-icons:arrow-cycle"),
    ],
    className="metrics",
)

latex_formula = dl.DashLatex(
    r"""
    \(F = \alpha A + \beta \frac{M}{Mmax} + \gamma \frac{T}{Tmax} + \delta \frac{W}{Wmax}\)
    """,
    
)

latex_formula = html.Div([
        # Your math formula goes here
        html.Div("$$\\frac{a}{b} = c$$", id="math-formula"),
    ])

latex_formula = dcc.Markdown('$$F = \\alpha Accuracy + \\beta \\frac{Memory Footprint}{Max Memory Footprint} + \\gamma \\frac{Inference Time}{Max Inference Time} + \\delta \\frac{Energy Consumption}{Max Energy Consumption}$$', mathjax=True)

fitness = html.Div(
    [
        dot_heading("Fitness parameters"),
        fitnes_function_latex(latex_formula), 
        metric_card("Max memory footprint", f'{hyperparams["max_memory_footprint"]} B', "fluent:memory-16-regular"),
        metric_card("Max inference time", f'{hyperparams["max_inference_time"]} ms', "uiw:time-o"),
        
        # Special Case for Meteos dataset
        metric_card("Max energy consumption", f'{hyperparams["max_energy_consumption"]} mJ', "simple-line-icons:energy") if "max_energy_consumption" in hyperparams else None, 
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

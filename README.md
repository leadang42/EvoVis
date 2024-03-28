# EvoVis

EvoVis is a dashboard for visualizing Evolutionary Neural Architecture Search (ENAS) algorithms. ENAS mimics biological evolution to discover optimal neural network architectures, starting with a population of randomly generated architectures and iteratively improving them through selection, crossover, and mutation. The key features of EvoVis are the following:

1. **Hyperparameter Overview:** Efficiently tune hyperparameters with an overview of settings.
2. **Gene Pool Graph:** Visualize potential neural architecture topologies and connectivity patterns across generations.
3. **Family Tree Graph:** Navigate the family tree of architectures, analyze performance metrics, and explore structures.
4. **Performance Plots:** Monitor performance trends in real-time with evolutionary metrics.
5. **Data Structure Interface:** Support for visualizing ENAS results from various frameworks and sources.

EvoVis offers a holistic view of the ENAS process. It provides insights into architectural evolution and performance optimization.

## Contents

- [EvoVis](#evovis)
  - [Contents](#contents)
  - [Getting Started](#getting-started)
  - [Compatible Algorithms](#compatible-algorithms)
  - [Data Structure Interface](#data-structure-interface)
  - [Project Organization](#project-organization)
  - [License](#license)
  - [Contact](#contact)


## Getting Started

1. **EvoVis Cloning:** Clone the EvoVis repository from [GitHub](https://github.com/leadang42/EvoVis.git) and navigate to the project directory.

````    
git clone https://github.com/leadang42/EvoVis.git
cd EvoVis
````

2. **EvoVis Dependencies:** Install the project's dependencies.
````    
pip install -r requirements.txt
````

3. **EvoVis Execution:** Run EvoVis by specifying your run results directory path or use the sample enas run in the enas_example_run_results directory.
````    
python EvoVis.py <run_results_path>
````
````
python EvoVis.py ./enas_example_run_results
````

4. **EvoVis Usage:** Access EvoVis dashboard via the provided localhost and explore hyperparameters, gene pool graph, family tree graph, and performance plots.

## Compatible Algorithms
1. **Gene Pool:** DAG-structured and one searchable level (e.g. no hierarchical search spaces) 
2. **Optimization Problems:** Multi-objective and single-objective 
3. **Selection:** All strategies
4. **Crossover:** One-point crossover strategy 
5. **Mutation:** All strategies


## Data Structure Interface
In order to visualize ENAS runs with EvoVis, the ENAS algorithm must output a run results directory that follows a specific data structure. Check out the `enas_example_run_results` directory as an example. Here's an overview of the required files:

`config.json`: Configuration settings for the ENAS algorithm's hyperparameters and measurements done on the neural architectures.

Settings for the `hyperparameters`
| Key | Description |
| --- | --- |
| `value` | The numerical value of the parameter. (Required) |
| `unit` | The unit of measurement for the parameter. |
| `icon` | The icon representing the parameter, for visual identification. |
| `displayname` | The human-readable name of the parameter. |
| `group` | The category to which the parameter belongs. |
| `description` | A brief description explaining the significance of the parameter. |

Settings for the `results`
| Key | Description |
| --- | --- |
| `displayname` | The human-readable name of the result metric. |
| `unit` | The unit of measurement for the result. |
| `run-result-plot` | Indicates whether to include the result in the aggregated results over generations plot in the run results page. |
| `individual-info-plot` | Indicates whether to include the result in individual information in the family tree page. |
| `pareto-optimlity-plot` | Indicates whether to include the result in the multi-objective mapping plot. |
| `individual-info-img` | The image representing the result found in `src/assets/media` directory. |
| `min-boundary` | The minimum boundary for valid result values. |
| `max-boundary` | The maximum boundary for valid result values. |

`crossover_parents.csv`: Information about offspring evolvement through crossover of two parents.


`search_space.json`:


`chromosome.json`:

`reslts.json`:

## Project Organization

![Image Name](/src/assets/media/project-organisation.png)

## License

EvoVis is licensed under the Apache License. See LICENSE file for details.

## Contact

For any inquiries or support, please contact [lea.van.anh.dang@gmail.com](mailto:lea.van.anh.dang@gmail.com).

---

EvoVis aims to visualize ENAS processes to provide researchers and practitioners with a comprehensive tool for understanding and optimizing neural architectures.

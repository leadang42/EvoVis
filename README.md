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
  - [Getting started](#getting-started)
  - [License](#license)
  - [Contact](#contact)


## Getting started

1. Clone the EvoVis repository from [GitHub](https://github.com/leadang42/EvoVis.git) and navigate to the project directory.

````    
git clone https://github.com/leadang42/EvoVis.git
cd EvoVis
````

2. Install the project's dependencies.
````    
pip install -r requirements.txt
````

3. Run EvoVis. The repository also contains a sample enas run in the enas_example_run_results directory.
````    
python EvoVis.py <run_results_path>
````
````
python EvoVis.py ./enas_example_run_results
````

4. Access EvoVis dashboard via the provided localhost and explore hyperparameters, gene pool graph, family tree graph, and performance plots.


## License

EvoVis is licensed under the Apache License. See LICENSE file for details.

## Contact

For any inquiries or support, please contact [lea.van.anh.dang@gmail.com](mailto:lea.van.anh.dang@gmail.com).

---

EvoVis aims to visualize ENAS processes to provide researchers and practitioners with a comprehensive tool for understanding and optimizing neural architectures.

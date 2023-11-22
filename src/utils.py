import pandas as pd
import os
import random

### READ HELPERS ###

def remove_comments(text):
    """Removes comments from a string"""

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.split('#', 1)[0].strip()
        if line: cleaned_lines.append(line)

    return '\n'.join(cleaned_lines) 

def txt_to_eval(filepath):
    """Converts a text file to dictionnairy"""
    json_data = None

    with open(filepath, 'r') as file:
        text = file.read()
        cleaned_text = remove_comments(text)
        json_data = eval(cleaned_text)

    return json_data


### NAMES OF DIRECTORIES ###

def get_runs():
    """Get all available runs"""
    run_path = f"../data"
    items = os.listdir(run_path)
    runs = [item for item in items if os.path.isdir(os.path.join(run_path, item))]

    runs.sort()

    return runs

def get_generations(run, as_int=False):
    """List of all generation names (dictionnairies) in run"""
    
    generation_path = f"../data/{run}"
    items = os.listdir(generation_path)
    generations = [item for item in items if os.path.isdir(os.path.join(generation_path, item))]
    generations_int = [int(gen.split("_")[1]) for gen in generations]

    generations_int.sort()

    if not as_int:
        return [f"Generation_{gen}" for gen in generations_int]
    else: 
        return [int(gen.split("_")[1]) for gen in generations]


### SIGNLE INDIVIDUAL INFORMATION ###

def get_individual_result(run, generation, individual):
    """Dict or None of individual's objective measurements"""
    path = f'../data/{run}/Generation_{generation}/{individual}/results.json'

    if os.path.isfile(path):
        return txt_to_eval(path)
    else:
        return None
    
def get_individual_chromosome(run, generation, individual):
    """List or None of individual's genes/ layers dicts"""

    path = f'../data/{run}/Generation_{generation}/{individual}/chromosome.json'

    if os.path.isfile(path):
        return txt_to_eval(path)
    else:
        return None

def get_individual_power_measurements(run, generation, individual):
    """List or None of individual's genes/ layers dicts"""
    path = f'../data/{run}/Generation_{generation}/{individual}/power_measurements.csv'

    if os.path.isfile(path):
        return pd.read_csv(path)
    else:
        return None
 
### INDIVIDUALS INFORMATION ###

def get_individuals_of_generation(run, generation, value="names"):
    """
    Get the data of all individuals of a specified generation.
    
    Args:
        run (str): The directory name of the run data.
        generation (int): Generation where genes will be counted.
        value (str): The data of an individual that will be accessed. Available are "names", "results", "chromosomes" or "power_measurements".
    
    Returns:
        individuals_names (list) or individual_dict (dict): Get the list of names if value is set to name or a dictionairy with individual names as keys.
    """
    
    # Assert in case of wrong input values
    available_values = ["names", "results", "chromosomes", "power_measurements"]
    generations = [int(gen.split("_")[1]) for gen in get_generations(run)]
    
    assert value in available_values, "Unavailable return value"
    assert generation in generations, "Unavailable generation"
    
    # Access individuals names
    items = os.listdir(f"../data/{run}/Generation_{generation}")
    individuals_names = [item for item in items if os.path.isdir(os.path.join(f"../data/{run}/Generation_{generation}", item))]

    if value == "names":
        individuals_names.sort()
        return individuals_names
    
    # Access individuals data
    individual_dict = {}

    for individual in individuals_names:

        if value == "results":
            individual_dict[individual] = get_individual_result(run, generation, individual)
        
        elif value == "chromosomes":
            individual_dict[individual] = get_individual_chromosome(run, generation, individual)

        elif value == "power_measurements":
            individual_dict[individual] = get_individual_power_measurements(run, generation, individual)
    
    return individual_dict

def get_individuals(run, generation_range=None, value="names", as_generation_dict=False):
    """
    Get data from the indivduals of a generation range or all the generations. 
    
    Args: 
        run (str): The directory name of the run data.
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        value (str): The return values of the individuals. Choose between the values "names", "results", "chromosomes" or "power_measurements".
        as_generation_dict (bool): Specify if individuals 
        
    Returns:
        generations (dict) or individuals (list): Outputs a dict with generation key (in int) containing dict with individual key or a list only with the values (no generation, individualname specifications). 
    """
    
    # (No assertion needed bc of helper function)

    # Generation range creation in case of None
    generation_range = range(1, len(get_generations(run)) + 1) if generation_range is None else generation_range
    
    if as_generation_dict:
        
        generations = {}
        for generation in generation_range:
            generations[generation] = get_individuals_of_generation(run, generation, value)
    
        return generations
    
    else: 
        
        individuals = []
        for generation in generation_range:
            if value != "names":
                individuals += list(get_individuals_of_generation(run, generation, value).values())
            else:
                individuals += get_individuals_of_generation(run, generation, value)

        return individuals
    
def get_individuals_best_result(run, generation_range=None, measure="val_acc"):
    """
    Get the best results of all individuals of a generation range. 
    
    Args:
        run (str): The directory name of the run data.
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        measure (str): Choose the measure you want to comapre. Select between "val_acc", "memory_footprint_h5", "memory_footprint_tflite", "memory_footprint_c_array", "inference_time", "energy_consumption", "mean_power_consumption", "fitness".
        
    Returns:
        generation (int): Generation with best result.
        individual (str): Individual with best result.
        best_value (float): The best result of all individuals in given generation rangee.
    """
    
    available_measures = ["val_acc", "memory_footprint_h5", "memory_footprint_tflite", "memory_footprint_c_array", "inference_time", "energy_consumption", "mean_power_consumption", "fitness"]
    assert measure in available_measures, "Unavailable measure value"
    
    values = get_individuals(run, generation_range, "results", as_generation_dict=True)
    
    best_value = 0 if (measure == "val_acc" or measure == "fitness") else 100000000
    generation = None
    individual = None
    
    for gen, results in values.items():
        for ind, result in results.items():
            
            if measure in result:
                val = result[measure]

                if type(val) == int or type(val) == float: 
                    
                    if val < best_value and measure != "val_acc" and measure != "fitness": generation, individual, best_value = gen, ind, val
                    if val > best_value and (measure == "val_acc" or measure == "fitness"): generation, individual, best_value = gen, ind, val
               
    return generation, individual, best_value           
  
def get_individuals_worst_result(run, generation_range=None, measure="val_acc"):
    """
    Get the worst results of all individuals of a generation range. 
    
    Args:
        run (str): The directory name of the run data.
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        measure (str): Choose the measure you want to comapre. Select between "val_acc", "memory_footprint_h5", "memory_footprint_tflite", "memory_footprint_c_array", "inference_time", "energy_consumption", "mean_power_consumption", "fitness".
        
    Returns:
        generation (int): Generation with best result 
        individual (str): Individual with best result 
        worst_value (float): The best result of all individuals in given generation range
    """
    
    available_measures = ["val_acc", "memory_footprint_h5", "memory_footprint_tflite", "memory_footprint_c_array", "inference_time", "energy_consumption", "mean_power_consumption", "fitness"]
    assert measure in available_measures, "Unavailable measure value"
    
    values = get_individuals(run, generation_range, "results", as_generation_dict=True)
    
    worst_value = 1 if (measure == "val_acc" or measure == "fitness") else 0
    generation = None
    individual = None
    
    for gen, results in values.items():
        for ind, result in results.items():
            
            if measure in result:
                val = result[measure]

                if type(val) == int or type(val) == float: 
                    
                    if val > worst_value and measure != "val_acc" and measure != "fitness": generation, individual, worst_value = gen, ind, val
                    if val < worst_value and (measure == "val_acc" or measure == "fitness"): generation, individual, worst_value = gen, ind, val
               
    return generation, individual, worst_value
  
def get_individuals_min_max(run, generation_range=None):
    values = get_individuals(run, generation_range, "results", as_generation_dict=True)
    
    measurements = {
        "val_acc": {
            'min': {'generation': None, 'individual': None, 'value': 1}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "memory_footprint_h5": {
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "memory_footprint_tflite": {
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "memory_footprint_c_array":{
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "inference_time": {
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "energy_consumption": {
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "mean_power_consumption": {
            'min': {'generation': None, 'individual': None, 'value': 1000000000}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }, 
        "fitness": {
            'min': {'generation': None, 'individual': None, 'value': 1}, 
            'max': {'generation': None, 'individual': None, 'value': 0}
        }
    }
    
    for gen, results in values.items():
        for ind, result in results.items():
            
            for measure, min_max in measurements.items():
                if measure in result:
                    val = result[measure]
                
                    if type(val) == int or type(val) == float: 
                        
                        if val < min_max['min']['value']: 
                            measurements[measure]['min'] = {'generation': gen, 'individual': ind, 'value': val}
                            
                        if val > min_max['max']['value']: 
                            measurements[measure]['max'] = {'generation': gen, 'individual': ind, 'value': val}
                
    return measurements
    
  
def get_number_of_genes(run, generation, genename):
    """
    Get the number of genes in a certain generation.
    
    Args:
        run (str): The directory name of the run data.
        generation (int): Generation where genes will be counted.
        genename (str): The "layer" identifier of the a gene. 
        
    Returns:
        count (int): Number of genes
    """
    chromosomes = get_individuals(run, range(generation, generation+1), value="chromosomes", as_generation_dict=False)

    count = 0
    for chromosome in chromosomes:
        for gene in chromosome:

            if gene["layer"] == genename:
                count += 1

    return count

### RUN INFORMATION ###

def get_hyperparamters(run):
    """Dict of hyperparameters of EvoNAS run"""
    return txt_to_eval(f'../data/{run}/params.json')


### GENEPOOL ###
# TODO Lock classes and start

preprocessing = ['STFT', 'MAG', 'MEL', 'MAG2DEC']
one_dim_feature = ['C_1D', 'DC_1D', 'MP_1D', 'AP_1D', 'R_1D', 'BN_1D', 'IN_1D']
two_dim_feature = ['C_2D', 'DC_2D', 'MP_2D', 'AP_2D', 'R_2D', 'BN_2D', 'IN_2D']
one_dim_global_pooling = ['GAP_1D', 'GMP_1D']
two_dim_global_pooling = ['GAP_2D', 'GMP_2D']
dense = ['DO', 'D']

layers_type = {}

for p in preprocessing: layers_type[p] = "Preprocessing Layer"
for fo in one_dim_feature: layers_type[fo] = "1D Feature Layer"
for ft in two_dim_feature: layers_type[ft] = "2D Feature Layer"
for go in one_dim_global_pooling: layers_type[go] = "1D Global Pooling Layer"
for gt in two_dim_global_pooling: layers_type[gt] = "2D Global Pooling Layer"
for d in dense: layers_type[d] = "Dense Layer"

def get_genepool(run, get_dict=False):
    """List of genes dicts or dict with layerid as keys"""
    genes = txt_to_eval(f'../data/{run}/gene_pool.txt')
    genes_dict = {}

    if not get_dict:
        return genes

    for gene in genes:
        genes_dict[gene['layer']] = gene

    return genes_dict

def get_ruleset(run, cytoscape_dag=True, exclude_unreachable=True):
    """List of nodes and edges for element param in cytoscape"""

    # Read ruleset
    ruleset = txt_to_eval(f'../data/{run}/rule_set.txt')
    genepool = get_genepool(run, get_dict=True)

    # Return list of ruleset
    if not cytoscape_dag:
        return ruleset
    
    # Create cytoscape with layer types
    nodes = [
        { 'data': {'id': 'pr', 'label': 'Preprocessing'} },
        { 'data': {'id': 'fe', 'label': 'Feature Extraction'} },
        { 'data': {'id': 'gl', 'label': 'Global Pooling'} },
        { 'data': {'id': 'de', 'label': 'Dense'} },
        { 'data': {'id': 'end', 'label': 'End', 'f_name': 'End', 'layer': 'End', 'ltype': 'End'} }
    ]
    edges = [
        { 'data': {'id':'feature-globalpooling', 'source': 'fe', 'target': 'gl'}, 'classes': 'class-connect' },
        { 'data': {'id':'dense-end', 'source': 'de', 'target': 'end'}, 'classes': 'class-connect' },
    ]
    
    # Create cytoscape starting point
    lallowed = dense
    
    for rule in ruleset:
            
        if rule['layer'] == 'Start':
            nodes.append({ 'data': {'id': 'Start', 'label': 'Start', 'f_name': 'Start', 'layer': 'Start', 'ltype': 'Start'} })

            for start_with in rule['start_with']:
                edges.append({
                    'data': {'source': rule['layer'], 'target': start_with}, 
                    'classes': f'{rule["layer"]} {start_with}'
                })
                
                if start_with in preprocessing: 
                    lallowed += preprocessing + two_dim_feature + two_dim_global_pooling
                    
                else: 
                    lallowed += one_dim_feature + one_dim_global_pooling

    # After analysing start continue with rest
    for rule in ruleset:
        
        layer = rule['layer']
        
        # Skip Start layer (already processed)
        if layer == 'Start':
            continue
        
        # Layers that are of the right dimension
        elif layer in lallowed:
            
            genepool[layer]['id'] = layer
            genepool[layer]['label'] = layer.replace('_', ' ')
            genepool[layer]['ltype'] = layers_type[layer]
            
            # Layer Category
            if layer in preprocessing: 
                genepool[layer]['parent'] = 'pr'
            elif layer in (one_dim_feature + two_dim_feature): 
                genepool[layer]['parent'] = 'fe'
            elif layer in (one_dim_global_pooling + two_dim_global_pooling): 
                genepool[layer]['parent'] = 'gl'
            elif layer in dense: 
                genepool[layer]['parent'] = 'de'
            
            nodes.append({ 'data': genepool[rule['layer']] })

            for allowed_after in rule['allowed_after']:
                
                if allowed_after in lallowed:
                    edges.append({
                        'data': {'source': layer, 'target': allowed_after}, 
                        'classes': f'{layer} {allowed_after}'
                    })
        
    elements = nodes + edges
    return elements

def get_start_gene(run):
    """Dict of start gene"""
    ruleset = get_ruleset(run, cytoscape_dag=False)
    genepool = get_genepool(run, get_dict=True)

    for rule in ruleset:
        if rule['layer'] == 'Start':
            return genepool[rule['start_with'][0]]
     
        
### INDIVIDUAL CREATION ###
# TODO Deprecate crossover dict
       
def get_best_individuals(run):
    """Dataframe of parents of individuals"""

    df = pd.read_csv(f'../data/{run}/best_individual_each_generation.csv', header=None)
    df = df.rename(columns={0:"Generation", 1:"Individual", 2:"Fitness"})
    df = df.reindex(columns=["Generation", "Individual", "Fitness"])

    df["Generation"] = df["Generation"].str.replace("Generation_", "")
    df["Generation"] = df["Generation"].astype('int64')

    return df

def get_crossover_parents(run):
    """Dicitionnairy with key individual and values of parents of individuals with values=["Generation", "New Individual", "Parent 1", "Crossover 1", "Parent 2", "Crossover 2"]"""

    df = pd.read_csv(f'../data/{run}/crossover_parents.csv', header=None)
    df = df.rename(columns={0:"Generation", 1:"Parent 1", 2:"Parent 2", 3:"New Individual"})
    df = df.reindex(columns=["Generation", "New Individual", "Parent 1", "Crossover 1", "Parent 2", "Crossover 2"])

    crossover_dict = {}

    for idx, row in df.iterrows():
        individual = row["New Individual"].replace("New_Individual: ", "")

        generation = int(row["Generation"].replace("Generation: ", ""))
        parent1 = row["Parent 1"].replace("Parent_1: ", "").replace("(", "").replace(")", "")
        parent2 = row["Parent 2"].replace("Parent_2: ", "").replace("(", "").replace(")", "")

        parent1, crossover1 = parent1.split(",")[0], parent1.split(",")[1]
        parent2, crossover2 = parent2.split(",")[0], parent2.split(",")[1]

        crossover_dict[individual] = {
            "generation": generation,
            "parent1": parent1,
            "crossover1": crossover1, 
            "parent2": parent2,
            "crossover2": crossover2, 
        }

    return crossover_dict

def get_crossover_parents_df(run):
    """
    Dataframe of parents of individuals (not in use)
    
    Args:
        run (str): The directory name of the run data.
        
    Returns:
        df (pandas.DataFrame): Dataframe with columns ["generation", "individual", "parent1", "crossover1", "parent2", "crossover2"]
    """

    df = pd.read_csv(f'../data/{run}/crossover_parents.csv', header=None)
    df = df.rename(columns={0:"generation", 1:"parent1", 2:"parent2", 3:"individual"})
    df = df.reindex(columns=["generation", "individual", "parent1", "crossover1", "parent2", "crossover2"])

    df["generation"] = df["generation"].str.replace("Generation: ", "")
    df["parent1"] = df["parent1"].str.replace("Parent_1: ", "")
    df["parent2"] = df["parent2"].str.replace("Parent_2: ", "")
    df["individual"] = df["individual"].str.replace("New_Individual: ", "")

    df["generation"] = df["generation"].astype('int64')

    for idx, row in df.iterrows():
       
        p1 = row["parent1"].replace("(", "").replace(")", "")
        p2 = row["parent2"].replace("(", "").replace(")", "")

        df.loc[idx, "parent1"] = p1.split(",")[0]
        df.loc[idx, "crossover1"] = p1.split(",")[1]
        df.loc[idx, "parent2"] = p2.split(",")[0]
        df.loc[idx, "crossover2"] = p2.split(",")[1]

    return df        


### FAMILY TREE GENERATION ###
# TODO Change node data into individual data

def get_upstream_tree(run, generation, individual, generation_range):
    """
    Helper funnction for family tree: Create upstream famliy tree with nodes, edges and root elements starting from selected individual.
    
    Args:
        run (str): The directory name of the run data.
        generation (int): Generation of individual
        individual (str): Individual from where family tree evolves from. 
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        
    Returns:
        elements (list): List of nodes and edges for element param in cytoscape.
        root (list): List of roots nodes to create right tree structure.
    """
    
    min_generation = generation_range[0]

    # End condition with only one individual
    if min_generation == generation:
        return ([{'data': {'id': individual, 'label': individual[0:3], 'generation': generation, 'extinct': False}}], [individual])

    # Nodes and edges for individual
    crossovers = get_crossover_parents(run)
    
    parent1 = crossovers[individual]["parent1"]
    crossover1 = crossovers[individual]["crossover1"]
    
    parent2 = crossovers[individual]["parent2"]
    crossover2 = crossovers[individual]["crossover2"]

    individual_el = [
        {'data': {'id': individual, 'label': individual[0:3], 'generation': generation, 'extinct': False}},
        {'data': {'source': parent1, 'target': individual, 'edgelabel': crossover1}},
        {'data': {'source': parent2, 'target': individual, 'edgelabel': crossover2}}
    ]

    # Recursion for moving up the tree
    parent1_tree, roots1 = get_upstream_tree(run, generation-1, parent1, generation_range)
    parent2_tree, roots2 = get_upstream_tree(run, generation-1, parent2, generation_range)

    return (parent1_tree + individual_el + parent2_tree, roots1 + roots2)

def get_downstream_tree(run, generation, individual, generation_range):
    """
    Helper funnction for family tree: Create upstream famliy tree with nodes and edges starting from selected individual.
    
    Args:
        run (str): The directory name of the run data.
        generation (int): Generation of individual
        individual (str): Individual from where family tree evolves from. 
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        
    Returns:
        elements (list): list of nodes and edges for element param in cytoscape.
    """

    max_generation = generation_range[-1]
    
    # Get children of individual
    crossovers = get_crossover_parents_df(run)
    children = list(crossovers[crossovers['parent1'].str.contains(individual)]["individual"].values)
    crossover = list(crossovers[crossovers['parent1'].str.contains(individual)]["crossover1"].values)
    
    children += list(crossovers[crossovers['parent2'].str.contains(individual)]["individual"].values)
    crossover += list(crossovers[crossovers['parent2'].str.contains(individual)]["crossover2"].values)
    
    extinct = False if children else True

    # End condition with only one individual
    if max_generation == generation:
        return [{'data': {'id': individual, 'label': individual[0:3], 'generation': generation, 'extinct': extinct}}]

    # Nodes and edges for individual
    individual_el = [{'data': {'id': individual, 'label': individual[0:3], 'generation': generation, 'extinct': extinct}}]

    for idx, child in enumerate(children):
        individual_el.append({'data': {'source': individual, 'target': child, 'edgelabel': crossover[idx]}})

    # Recursion for moving down the tree
    children_tree = []

    for child in children: 
        children_tree += get_downstream_tree(run, generation+1, child, generation_range)

    return children_tree + individual_el

def get_family_tree(run, generation, individual, generation_range=None):
    """
    Create famliy tree with nodes, edges and roots elements starting from selected individual.
    
    Args:
        run (str): The directory name of the run data.
        generation (int): Generation of individual
        individual (str): Individual from where family tree evolves from. 
        generation_range (range): A python range of generations from which the individuals will be extracted. 
        
    Returns:
        elements (list): list of nodes and edges for element param in cytoscape.
        root (list): List of roots nodes to create right tree structure.
    """

    # Set default value
    if generation_range is None:
        generation_range = range(generation-2, generation+1)

    # Get the entire tree without duplicates
    upstream_tree, roots = get_upstream_tree(run, generation, individual, generation_range)
    downstream_tree = get_downstream_tree(run, generation, individual, generation_range)

    family_tree = []
    unique_roots = []

    for el in downstream_tree + upstream_tree:
        if el not in family_tree: family_tree.append(el)

    for el in roots:
        if el not in unique_roots: unique_roots.append(el)
    
    return (family_tree, unique_roots)


### OTHER HELPER FUNCTIONS ###

def get_random_individual(run, generation=None):
    """Get the first sorted individual from a random generation of specified run."""
    if generation is None:
        generations = get_generations(run)
        generation = random.choice(generations)
        generation = int(generation.split("_")[1])
    
    individuals = get_individuals(run, range(generation, generation+1), value="names", as_generation_dict=False)
    
    return generation, individuals[0]

def report():
    run = "ga_20230116-110958_sc_2d_4classes"
    generation = 1
    individual = "abstract_wildebeest"
    
    print("Best Results:")
    print("--------------------------------")
    print("Best Accuracy: ", get_individuals_best_result(run, None, "val_acc"))
    print("Best Footprint: ", get_individuals_best_result(run, None, "memory_footprint_h5"))
    print("Best Footprint: ", get_individuals_best_result(run, None, "memory_footprint_tflite"))
    print("Best Footprint: ", get_individuals_best_result(run, None, "memory_footprint_c_array"))
    print("Best Inference Time: ", get_individuals_best_result(run, None, "inference_time"))
    print("Best Energy Consumption: ", get_individuals_best_result(run, None, "energy_consumption"))
    print("Best Fitness: ", get_individuals_best_result(run, None, "fitness"))
    print()
    
    print("Worst Results:")
    print("--------------------------------")
    print("Worst Accuracy: ", get_individuals_worst_result(run, None, "val_acc"))
    print("Worst Footprint: ", get_individuals_worst_result(run, None, "memory_footprint_h5"))
    print("Worst Footprint: ", get_individuals_worst_result(run, None, "memory_footprint_tflite"))
    print("Worst Footprint: ", get_individuals_worst_result(run, None, "memory_footprint_c_array"))
    print("Worst Inference Time: ", get_individuals_worst_result(run, None, "inference_time"))
    print("Worst Energy Consumption: ", get_individuals_worst_result(run, None, "energy_consumption"))
    print("Worst Fitness: ", get_individuals_worst_result(run, None, "fitness"))
    print()
    
    print("Random Individuals:")
    print("--------------------------------")
    print("Random Individual: ", get_random_individual(run)[1], "-> Generation: ", get_random_individual(run)[0])
    
    measurements = get_individuals_min_max(run, None)
    print(measurements)
    
    for key, value in measurements.values():
        print(key)
        print(value)
        print()
              
#report()
import pandas as pd
import os

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

def get_generations(run):
    """List of all generation names (dictionnairies) in run"""
    
    generation_path = f"../data/{run}"
    items = os.listdir(generation_path)
    generations = [item for item in items if os.path.isdir(os.path.join(generation_path, item))]

    generations.sort()

    return generations


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

def get_individuals_of_generation(run, generation, value="name"):
    """List of individuals' "names" or dict or list of "results", "chromosomes" or "power_measurements" for one generation"""

    items = os.listdir(f"../data/{run}/Generation_{generation}")
    individuals_names = [item for item in items if os.path.isdir(os.path.join(f"../data/{run}/Generation_{generation}", item))]

    if value == "name":
        return individuals_names
    
    individual_dict = {}

    for individual in individuals_names:

        if value == "results":
            individual_dict[individual] = get_individual_result(run, generation, individual)
        
        elif value == "chromosomes":
            individual_dict[individual] = get_individual_chromosome(run, generation, individual)

        elif value == "power_measurements":
            individual_dict[individual] = get_individual_power_measurements(run, generation, individual)
    
    return individual_dict


def get_individuals(run, generation_range=None, value="name", as_generation_dict=False):
    """List of individuals' "names", "results", "chromosomes" or "power_measurements" for generation range"""

    generation_range = range(1, len(get_generations(run)) + 1) if generation_range is None else generation_range
    
    if as_generation_dict:
        generations = {}

        for generation in generation_range:
            generations[generation] = get_individuals_of_generation(run, generation, value)
    
        return generations
    
    else: 
        individuals = []

        for generation in generation_range:

            individuals += list(get_individuals_of_generation(run, generation, value).values())
            print(list(get_individuals_of_generation(run, generation, value).values()))

        return individuals
    

def get_number_of_genes(run, generation, genename):
    """Outputs number of genes in a certain generation"""
    chromosomes = get_individuals(run, range(generation, generation+1), value="chromosomes", as_generation_dict=False)

    count = 0
    for chromosome in chromosomes:

        for gene in chromosome:

            if gene["layer"] == genename:
                count += 1

    return count


### RUN INFORMATION ###
# TODO Deprecate crossover dict

def get_hyperparamters(run):
    """Dict of hyperparameters of EvoNAS run"""
    return txt_to_eval(f'../data/{run}/params.json')


def get_genepool(run):
    """List of genes dicts"""
    return txt_to_eval(f'../data/{run}/gene_pool.txt')


def get_ruleset(run, cytoscape_dag=True):
    """List of nodes and edges for element param in cytoscape"""

    ruleset = txt_to_eval(f'../data/{run}/rule_set.txt')

    if not cytoscape_dag:
        return ruleset
    
    nodes = []
    edges = []

    for rule in ruleset:

        # Start layer
        if rule['layer'] == 'Start':
            nodes.append({ 'data': {'id': rule['layer'], 'label': rule['layer']}})

            for start_with in rule['start_with']:
                edges.append({'data': {'source': rule['layer'], 'target': start_with}})

        # Not start layers
        else:
            nodes.append({ 'data': {'id': rule['layer'], 'label': rule['layer'].replace('_', ' ')}})

            for allowed_after in rule['allowed_after']:
                edges.append({'data': {'source': rule['layer'], 'target': allowed_after}})
        
    elements = nodes + edges
    return elements


def get_best_individuals(run):
    """Dataframe of parents of individuals"""

    df = pd.read_csv(f'../data/{run}/best_individual_each_generation.csv', header=None)
    df = df.rename(columns={0:"Generation", 1:"Individual", 2:"Fitness"})
    df = df.reindex(columns=["Generation", "Individual", "Fitness"])

    df["Generation"] = df["Generation"].str.replace("Generation_", "")
    df["Generation"] = df["Generation"].astype('int64')

    return df


def get_crossover_parents(run):
    """Dicitionnairy of parents of individuals with values=["Generation", "New Individual", "Parent 1", "Crossover 1", "Parent 2", "Crossover 2"]"""

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
    """Dataframe of parents of individuals (not in use)"""

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

def get_upstream_tree(run, generation, individual, generation_range, x_max=1000, y_max=1000):
    """Get upstream individuals of an individual until stop generation with maybe duplicate nodes"""

    min_generation = generation_range[0]

    # End condition with only one individual
    if min_generation == generation:
        return ([{'data': {'id': individual, 'label': individual[0:3]}}], [individual])

    # Nodes and edges for individual
    crossovers = get_crossover_parents(run)
    parent1 = crossovers[individual]["parent1"]
    parent2 = crossovers[individual]["parent2"]

    individual_el = [
        {'data': {'id': individual, 'label': individual[0:3]}},
        {'data': {'source': parent1, 'target': individual}},
        {'data': {'source': parent2, 'target': individual}}
    ]

    # End condition woith nodes for parents
    if min_generation == generation-1:

        parent1_el = [{'data': {'id': parent1, 'label': parent1[0:3]}}]
        parent2_el = [{'data': {'id': parent2, 'label': parent2[0:3]}}]

        return (parent1_el + individual_el + parent2_el, [parent1, parent2])

    # Recursion for moving up the tree
    parent1_tree, roots1 = get_upstream_tree(run, generation-1, parent1, generation_range)
    parent2_tree, roots2 = get_upstream_tree(run, generation-1, parent2, generation_range)

    return (parent1_tree + individual_el + parent2_tree, roots1 + roots2)


def get_downstream_tree(run, generation, individual, generation_range, x_max=1000, y_max=1000):
    """Get children of an individual"""

    max_generation = generation_range[-1]

    # End condition with only one individual
    if max_generation == generation:
        return [{'data': {'id': individual, 'label': individual[0:3]}}]

    # Nodes and edges for individual
    crossovers = get_crossover_parents_df(run)
    
    children = crossovers[crossovers['parent1'].str.contains(individual) | crossovers['parent2'].str.contains(individual)]
    children = list(children["individual"].values)

    individual_el = [{'data': {'id': individual, 'label': individual[0:3]}}]

    for child in children:
        individual_el.append({'data': {'source': individual, 'target': child}})

    # End condition with nodes for children
    if max_generation == generation+1:
        children_el = [{'data': {'id': child, 'label': child[0:3]}} for child in children]
        return individual_el + children_el
    
    # Recursion for moving down the tree
    children_tree = []

    for child in children: 
        children_tree += get_downstream_tree(run, generation+1, child, generation_range)

    return children_tree + individual_el


def get_family_tree(run, generation, individual, generation_range=None):
    """List of nodes and edges for element param in cytoscape"""

    # Set default value
    if generation_range is None:
        generation_range = range(generation-2, generation+1)

    # Get the entire tree without duplicates
    upstream_tree, roots = get_upstream_tree(run, generation, individual, generation_range)
    downstream_tree = get_downstream_tree(run, generation, individual, generation_range)

    family_tree = []
    unique_roots = []

    for el in upstream_tree + downstream_tree:
        if el not in family_tree: family_tree.append(el)

    for el in roots:
        if el not in unique_roots: unique_roots.append(el)
    
    return (family_tree, unique_roots)




run = "ga_20230116-110958_sc_2d_4classes"
generation = 1
individual = "abstract_wildebeest"

#print(get_number_of_genes(run, generation, 'C_2D'))

#print(get_individual_chromosome(run, generation, individual))
import pandas as pd

# TODO Deprecate crossover dict
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
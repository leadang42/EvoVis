import pandas as pd
import os

def remove_comments(text):
    """Removes comments from a string"""

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.split('#', 1)[0].strip()
        if line: cleaned_lines.append(line)

    return '\n'.join(cleaned_lines) 


def txt_to_dict(filepath):
    """Converts a text file to dictionnairy"""
    json_data = None

    with open(filepath, 'r') as file:
        text = file.read()
        cleaned_text = remove_comments(text)
        json_data = eval(cleaned_text)

    return json_data


def hyperparamters(run):
    """Dict of hyperparameters of EvoNAS run"""
    return txt_to_dict(f'../data/{run}/params.json')


def genepool(run):
    """List of genes dicts"""
    return txt_to_dict(f'../data/{run}/gene_pool.txt')


def ruleset(run):
    """List of rules dicts"""
    return txt_to_dict(f'../data/{run}/rule_set.txt')


def crossover_parents(run):
    """Dataframe of parents of individuals"""

    df = pd.read_csv(f'../data/{run}/crossover_parents.csv', header=None)
    df = df.rename(columns={0:"Generation", 1:"Parent 1", 2:"Parent 2", 3:"New Individual"})
    df = df.reindex(columns=["Generation", "New Individual", "Parent 1", "Crossover 1", "Parent 2", "Crossover 2"])

    df["Generation"] = df["Generation"].str.replace("Generation: ", "")
    df["Parent 1"] = df["Parent 1"].str.replace("Parent_1: ", "")
    df["Parent 2"] = df["Parent 2"].str.replace("Parent_2: ", "")
    df["New Individual"] = df["New Individual"].str.replace("New_Individual: ", "")

    df["Generation"] = df["Generation"].astype('int64')

    for idx, row in df.iterrows():
       
        p1 = row["Parent 1"].replace("(", "").replace(")", "")
        p2 = row["Parent 2"].replace("(", "").replace(")", "")

        df.loc[idx, "Parent 1"] = p1.split(",")[0]
        df.loc[idx, "Crossover 1"] = p1.split(",")[1]
        df.loc[idx, "Parent 2"] = p2.split(",")[0]
        df.loc[idx, "Crossover 2"] = p2.split(",")[1]

    return df

def best_individuals(run):
    """Dataframe of parents of individuals"""

    df = pd.read_csv(f'../data/{run}/best_individual_each_generation.csv', header=None)
    df = df.rename(columns={0:"Generation", 1:"Individual", 2:"Fitness"})
    df = df.reindex(columns=["Generation", "Individual", "Fitness"])

    df["Generation"] = df["Generation"].str.replace("Generation_", "")
    df["Generation"] = df["Generation"].astype('int64')

    return df


def individual_result(run, generation, individual):
    """Dict or None of individual's objective measurements"""
    path = f'../data/{run}/Generation_{generation}/{individual}/results.json'

    if os.path.isfile(path):
        return txt_to_dict(path)
    else:
        return None

def individual_chromosome(run, generation, individual):
    """List or None of individual's genes/ layers dicts"""

    path = f'../data/{run}/Generation_{generation}/{individual}/chromosome.json'

    if os.path.isfile(path):
        return txt_to_dict(path)
    else:
        return None


def individual_power_measurements(run, generation, individual):
    """List or None of individual's genes/ layers dicts"""
    path = f'../data/{run}/Generation_{generation}/{individual}/power_measurements.csv'

    if os.path.isfile(path):
        return pd.read_csv(path)
    else:
        return None


def generations(run):
    """List of all generation names (dictionnairies) in run"""
    
    generation_path = f"../data/{run}"
    items = os.listdir(generation_path)
    generations = [item for item in items if os.path.isdir(os.path.join(generation_path, item))]

    generations.sort()

    return generations


def individuals_of_generation(run, generation, value="name"):
    """List of individuals' "names" or dict of "results", "chromosomes" or "power_measurements" for one generation"""

    items = os.listdir(f"../data/{run}/Generation_{generation}")
    individuals = [item for item in items if os.path.isdir(os.path.join(f"../data/{run}/Generation_{generation}", item))]

    if value == "name":
        return individuals
    
    individual_dict = {}

    for individual in individuals:

        if value == "results":
            individual_dict[individual] = individual_result(run, generation, individual)
        
        elif value == "chromosomes":
            individual_dict[individual] = individual_chromosome(run, generation, individual)

        elif value == "power_measurements":
            individual_dict[individual] = individual_power_measurements(run, generation, individual)
            
    return individual_dict


def individuals(run, generation_range=None, value="name", as_generation_dict=True):
    """List of individuals' "names", "results", "chromosomes" or "power_measurements" for generation range"""

    generation_range = range(1, len(generations(run)) + 1) if generation_range is None else generation_range

    if as_generation_dict:
    
        generations = {}

        for generation in generation_range:
            generations[generation] = individuals_of_generation(run, generation, value)

        return generations

    else:
        individuals = []

        for generation in generation_range:
            individuals = individuals + individuals_of_generation(run, generation, value)

        return individuals
    

def dag(run):
    """List of edges as tuples with start and end (start, end)"""

    df = crossover_parents(run)
    generations = {}

    for idx, row in df.iterrows():

        edge1 = (row["Parent 1"], row["New Individual"])
        edge2 = (row["Parent 1"], row["New Individual"])

        if row["Generation"] not in generations:
            generations[row["Generation"]] = [edge1, edge2]

        else: 
            generations[row["Generation"]].append(edge1)
            generations[row["Generation"]].append(edge2)

    return generations


run = "ga_20230116-110958_sc_2d_4classes"
generation = 1
individual = "abstract_wildebeest"

l = individuals_of_generation(run, 1)
print(l)
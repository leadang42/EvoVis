
import os
import json

##########################################################################################

# MODULE ENAS DATA CHECK

# The Enas Data Check Module provides functionalities to the data structure of configurations and results of a given run.
# Parameters: run (str) The identifier for the run. This is used to construct the path to the search_space.json file.
# Returns: (str) A message suggesting improvements to the data structure if validation fails or an empty string if the data structure is valid.

###########################################################################################

def json_to_dict(filepath):
    """
    Convert JSON data from a file to a Python dictionary.

    Parameters:
        filepath (str): The path to the JSON file.

    Returns:
        dict: A Python dictionary representing the JSON data.

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If there is an issue decoding the JSON data.

    Example:
    >>> data = json_to_dict('example.json')
    """
    
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON data in file {filepath}: {e}")

def validate_hyperparameters(run):
    filepath = f"{run}/config.json"
    
    # Check if config.json exists
    if not os.path.exists(filepath):
        return "Error config.json file: Config file 'config.json' not found."
    
    # Check if the file is a JSON
    try:
        data = json_to_dict(filepath)
    except json.JSONDecodeError:
        return "Error config.json file: Invalid JSON format in config.json."
    
    # Check if 'hyperparameters' key exists
    if 'hyperparameters' not in data:
        return "Error config.json file: Missing 'hyperparameters' key in config.json."
    
    hyperparameters = data['hyperparameters']
    
    # Check if hyperparameters contain a dictionary as value
    if not isinstance(hyperparameters, dict):
        return "Error config.json file: Hyperparameters must be a dictionary."
    
    message = ""
    
    # Check each hyperparameter
    for hp, details in hyperparameters.items():
        
        if not isinstance(details, dict):
            message += f"Error config.json file: Hyperparameter '{hp}' details must be a dictionary.\n"
            continue
        
        # Check if 'value' key exists
        if 'value' not in details:
            message += f"Error config.json file: Missing 'value' key for hyperparameter '{hp}'.\n"
        
    return message

def validate_meas_info(run):
    return ""

def validate_search_space(run):
    
    filepath = f"{run}/search_space.json"
    
    ### CHECK FILE ###
    # Check if search_space.json exists
    if not os.path.exists(filepath):
        return "Error search_space.json file: Search spcae file 'search_space.json' not found."
    
    # Check if the file is a JSON
    try:
        data = json_to_dict(filepath)
    except json.JSONDecodeError:
        return "Error search_space.json file: Invalid JSON format in search_space.json."
    
    
    ### CHECK KEYS ###
    # Check 'gene_pool' key
    if 'gene_pool' not in data:
        return "Error search_space.json file: Missing 'gene_pool' key in search_space.json."
    
    gene_pool = data['gene_pool']
    
    if not isinstance(gene_pool, dict):
        return "Error config.json file: Gene pool must be a dictionary."
    
    # Check 'rule_set' key
    if 'rule_set' not in data:
        return "Error search_space.json file: Missing 'rule_set' key in search_space.json."
    
    rule_set = data['rule_set']
    
    if not isinstance(rule_set, list):
        return "Error config.json file: Rule set must be a list."
    
    # Check 'rule_set_group' key (doesn't need to exists if no group rules)
    rule_set_group = data.get('rule_set_group', [])
    
    if not isinstance(rule_set_group, list):
        return "Error config.json file: Rule set groups must be a list."

    ### CHECK DATA STRUCTURES ###
    message = ""
    
    # Check gene pool structure
    for group, genes in gene_pool.items():
        if not isinstance(genes, list):
            message += f"Error search_space.json file: Gene pool '{group}' must be a list.\n"
        else:
            for gene in genes:
                if not isinstance(gene, dict):
                    message += f"Error search_space.json file: Gene in '{group}' must be a dictionary.\n"
                elif 'layer' not in gene:
                    message += f"Error search_space.json file: Gene in '{group}' is missing 'layer' key.\n"
                elif 'f_name' not in gene:
                    message += f"Error search_space.json file: Gene in '{group}' is missing 'f_name' key.\n"
                    
    # Check rule set structure
    start_found = False
    
    for rule_entry in rule_set:
        if not isinstance(rule_entry, dict):
            message += "Error search_space.json file: Rule in 'rule_set' must be a dictionary.\n"
        elif 'layer' not in rule_entry:
            message += "Error search_space.json file: Rule entry in 'rule_set' is missing 'layer' key.\n"
        elif 'rule' not in rule_entry:
            message += "Error search_space.json file: Rule entry in 'rule_set' is missing 'rule' key.\n"
        else:
            if rule_entry['layer'] == "Start":
                start_found = True

    if not start_found:
        message += "Error search_space.json file: Rule entry with layer 'Start' is missing.\n"
        
    # Check rule set group structure
    for group_entry in rule_set_group:
        if not isinstance(group_entry, dict):
            message += "Error search_space.json file: Group rule in 'rule_set_group' must be a dictionary.\n"
        elif 'group' not in group_entry:
            message += "Error search_space.json file: Group rule entry in 'rule_set_group' is missing 'layer' key.\n"
        elif 'rule' not in group_entry:
            message += "Error search_space.json file: Group rule entry in 'rule_set_group' is missing 'rule' key.\n"
    
    return message

def validate_crossover_parents(run):
    return ""

def validate_individual_results(run):
    return ""

def validate_individual_chromosomes(run):
    return ""

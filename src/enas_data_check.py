
import os
import json

##########################################################################################

# MODULE ENAS DATA CHECK

# The Enas Data Check Module provides functionalities for ...

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
    """
    Validate the structure of hyperparameters in a given run.

    Parameters:
        run (str): The identifier for the run. This is used to construct the path to the search_space.json file.

    Returns:
        str: A message suggesting improvements to the data structure if validation fails,
             or an empty string if the data structure is valid.

    """
    filepath = f"../data/{run}/config.json"
    
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
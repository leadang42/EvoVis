import json

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


def convert_json(json_data):
    converted_data = {
        "gene_pool": [],
        "rule_set": [],
        "rule_set_groups": []
    }

    # Convert gene_pool
    for group, layers in json_data["gene_pool"].items():
        for layer_data in layers:
            converted_layer = {
                "layer": layer_data["layer"],
                "f_name": layer_data["f_name"],
                "exclude": False,
                "group": group.replace("_", " ").title(),
            }
            for key, value in layer_data.items():
                if key not in ['layer', 'f_name', 'group', 'exclude']:
                    converted_layer[key] = value
            converted_data["gene_pool"].append(converted_layer)

    # Convert rule_set
    for key, value in json_data["rule_set"].items():
        for rule in value["rule"]:
            converted_rule = {
                "layer": key,
                "allowed_after": value["rule"],
                "exclude": key != rule
            }
            converted_data["rule_set"].append(converted_rule)

    # Convert rule_set_group
    for group_data in json_data["rule_set_group"]:
        converted_group = {
            "group": group_data["group"].replace("_", " ").title(),
            "allowed_after": group_data["rule"],
            "exclude": False
        }
        converted_data["rule_set_groups"].append(converted_group)

    return converted_data

# Example usage:
json_data = json_to_dict("/Users/leadang/Documents/Bachelorarbeit/Coding/EvoNAS-Dashboard/data/nRF52840/search_space_rene.json")  
converted_json = convert_json(json_data)
print(converted_json)


# Writing dictionary to file
with open("converted.json", "w") as file:
    json.dump(converted_json, file, indent=4)

import json

### The module search space covers the data processing of search_space.json
### TODO The search space is constant from the start so maybe make search space constant variable

### READ DATA FROM SEARCH SPACE JSON ###

def json_to_dict(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        
    return data

def get_search_space(run):
    return json_to_dict(f"../data/{run}/search_space.json")

def get_groups(run):
    
    search_space = get_search_space(run)
    layer_dict = {}

    for layer_info in search_space["gene_pool"]:
        layer_id = layer_info["layer"]
        group_type = layer_info["group"]
    
        if group_type not in layer_dict:
            layer_dict[group_type] = []
    
        layer_dict[group_type].append(layer_id)
        
    return layer_dict
    
### GRAPH CREATED FROM RULESETS ### 
            
def get_layer_graph(run, group_connections=True):
    """
    Retrieves the layer graph based on the search space defined for a given run.

    Args:
        run (str): The identifier for the run.
        group_connections (bool, optional): If True, includes group connections in the graph. 
            Defaults to True.

    Returns:
        dict: A dictionary representing the layer graph. Keys are source layers, 
              and values are lists of target layers connected to the source layer.

    Example:
        >>> get_layer_graph("run_123")
        {'STFT_2D': ['MAG_2D'], 'MAG_2D': ['FB_2D'], 'FB_2D': ['C_2D', 'DC_2D', 'MAG2DEC_2D'], ...}
    """
    
    # Read search space from JSON
    search_space = get_search_space(run)
    
    # Store layer connections in dictionairy
    graph = {}
    
    # Process layers connections
    for layer_rule in search_space["rule_set"]:
        
        if not (layer_rule["exclude"] if "exclude" in layer_rule else False):
            
            # Identify source and target layers
            src_layer = layer_rule["layer"]
            target_layers = layer_rule["allowed_after"]
            
            graph[src_layer] = target_layers
    
    # Return graph withour group connections
    if not group_connections:
        return graph       
    
    # Process group connections
    for group_rule in search_space["rule_set_groups"]:
        
        # Identify source and target group
        for target_group in group_rule["allowed_after"]:
            
            source_groups = group_rule["group"]
            
            # Identify source and target layers in source and target groups
            groups = get_groups(run)
            srouce_layers = groups[source_groups]
            target_layers = groups[target_group]
            
            for src_layer in srouce_layers:
                
                if src_layer in graph:
                    graph[src_layer] += target_layers
                else:
                    graph[src_layer] = target_layers

    return graph

def get_group_graph(run):
    """
    Builds the group graph based on the search space defined for a given run.

    Args:
        run (str): The identifier for the run.

    Returns:
        dict: A dictionary representing the group graph. Keys are source groups, 
              and values are lists of target groups connected to the source group.

    Example:
        >>> get_group_graph("run_123")
        {'Feature Extraction 1D': ['Global Pooling 1D'], 'Feature Extraction 2D': ['Global Pooling 2D']}
    """
    
    # Read search space from JSON
    search_space = get_search_space(run)
    
    # Store groups connections in dictionairy
    group_graph = {}
    
    # Process group connections
    for group_rule in search_space["rule_set_groups"]:
        
        excluded = group_rule["exclude"] if "exclude" in group_rule else False
        
        if not excluded:
            
            # Identify source and target group
            source_group = group_rule["group"]
            target_groups = group_rule["allowed_after"]
            
            group_graph[source_group] = target_groups
        
    return group_graph
 
 
### CONNECTED LAYERS ### 
  
def dfs(graph, layer, visited, result):
    
    if layer not in visited:
        
        visited.add(layer)
        result.append(layer)
        
        for neighbor in graph.get(layer, []):
            dfs(graph, neighbor, visited, result) 

def get_connected_layers(run, start_layer):
    
    graph = get_layer_graph(run, group_connections=True)
    
    visited = set()
    result = []
    
    dfs(graph, start_layer, visited, result)
    return result
    

### DASH CYTOSCAPE FORMAT ###

def get_node_element(gene):
    
    # Node must be in gene
    layer = gene["layer"]
    node = gene.copy()
    
    node["id"] = layer
    node["label"] = layer.replace("_", " ")
    
    # Group is optional
    if "group" in gene:
        
        group = node.pop("group")
        node["parent"] = group

    return node

def get_cytoscape_elements(run):
    
    search_space = get_search_space(run)
    
    elements = [{'data': {'id': 'Start', 'label': 'Start', 'f_name': 'Start', 'layer': 'Start'}}]
    group_elements = []
    groups = []

    # Use connected layers to create nodes of layers and groups
    start_layer = "Start"
    connected_layers = get_connected_layers(run, start_layer)
    
    genes = search_space["gene_pool"]
        
    for gene in genes:
        
        layer = gene["layer"]
        excluded = gene["exclude"] if "exclude" in gene else True
        
        if not excluded and layer in connected_layers:
            
            # Add layer node 
            layer_data = get_node_element(gene)
            element = { "data": layer_data }
            
            if element not in elements:
                elements.append(element)
            
            # Add group node 
            group = gene["group"] if "group" in gene else False
            
            if group:
                
                group_data = {'id': group, 'label': group}
                element = { "data": group_data }
                
                if element not in elements:
                    group_elements.append(element)
                    groups.append(group)
                    
    elements = group_elements + elements
    
    g = get_layer_graph(run, group_connections=False)
    
    for layer, edges in g.items():
        for edge in edges:
            element = { 'data': {'source': layer, 'target': edge},  'classes': f'{layer} {edge}' } 
            
            if element not in elements and layer in connected_layers:
                elements.append(element)
        
    group_graph = get_group_graph(run)
    
    for group_source, group_targets in group_graph.items():
        for group_target in group_targets:
            
            element = { 'data': {'source': group_source, 'target': group_target}, 'classes': 'class-connect' }
            
            if element not in elements and group_source in groups:
                elements.append(element)
    
    return elements, groups

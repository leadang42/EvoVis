
### NOT IN USE ###

def get_individuals():
    print("Place here")

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
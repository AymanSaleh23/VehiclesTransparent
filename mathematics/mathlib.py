
def map_values_ranges(input_value, input_range_min, input_range_max, output_range_min, output_range_max):
    return (input_value - input_range_min) * (output_range_max - output_range_min) / (input_range_max - input_range_min) + output_range_min;




#########       Test     ##########
print (map_values_ranges(0, 0, 180, 2, 12))

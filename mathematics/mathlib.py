
from math import pi, sin, cos, sqrt, radians
def map_values_ranges(input_value, input_range_min = 90, input_range_max = -90, output_range_min = 2, output_range_max = 12):
    return (input_value - input_range_min) * (output_range_max - output_range_min) / (input_range_max - input_range_min) + output_range_min;

def math_model (data = [[2,0],[2,-70],[3,80]], vehicle_lenght=4, direct_distance =4, theta = -50):
    
    #data is list of 3 lists
    #each list have [car_distance, car_angle]
        
    relatives = [ relative_dist[0] for  relative_dist in data]
    
    phis = [ angle[1] for angle in data]
    
    #alphas = [ (90- abs(theta) + (90-abs(phi)) ) for phi in phis]
    alphas = [0]*3
    #Tested for 9 cases of angels
    #####################################################
    #  Case   #   phis  #  theta   #  rule              #
    #####################################################
    #    1    #   +ve   #  +ve     #  180- phi + theta  #
    #    2    #   +ve   #  -ve     #  180-(phi + theta) #
    #    3    #   -ve   #  +ve     #  180-(phi + theta) #
    #    4    #   -ve   #  -ve     #  180- phi + theta  #
    #    5    #    0    #   0      #  180               #
    #    6    #    0    #  +ve     #  180 - phi         #
    #    7    #    0    #  -ve     #  180 - phi         #
    #    8    #    +ve  #   0      #  180 - theta       #
    #    9    #    -ve  #   0      #  180 - theta       #
    #####################################################
    
    for i in range(0,3):
        # Case 1, 4, 8, 9
        if (phis[i] > 0  and theta >= 0 ) or ( phis[i] < 0  and theta <= 0  ):
            alphas [i] = 180 - abs(phis[i]) +abs (theta)

        # Case 2, 3
        elif (phis[i] < 0  and theta > 0) or (phis[i] > 0  and theta < 0):
            alphas [i] = 180 - (abs(phis[i]) +abs (theta))

        # Case 5
        elif phis[i] == 0  and theta == 0:
            alphas[i] = 180
        
        # Case 6, 7
        elif (phis[i] == 0)  and  (theta >= 0 or theta < 0):
            alphas[i] = 180-abs(theta)
    
    #Tested over values
    b_lengths = [vehicle_lenght * abs(sin(radians(phis[i]))) / abs(sin(radians(alphas[i]))) for i in range(0,3) ]
    a_lengths = [vehicle_lenght * abs(sin(radians(theta))) / abs(sin(radians(alphas[i])))  for i in range (0,3)]
    
    #Tested
    total_lenght_X = [ relatives[i] + abs(b_lengths[i]) for i in range (0,3) ]
    total_lenght_Y = [ relatives[i] + abs(a_lengths[i]) for i in range (0,3) ]

    #Tested
    absolute_distances = [ round(sqrt( total_lenght_X[i]**2 + total_lenght_Y[i]**2 - 2 * total_lenght_X[i] * total_lenght_Y[i] * cos(radians(alphas[i])) ),4) for i in range(3)]
    return absolute_distances

#########       Test     ##########
print (map_values_ranges(-90, 90, -90, 2, 12))
print (math_model())
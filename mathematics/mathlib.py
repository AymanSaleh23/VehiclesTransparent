from math import sin, cos, sqrt, radians


def map_values_ranges(input_value, input_range_min=180, input_range_max=0, output_range_min=2, output_range_max=12):
    """
    Name        :   map_values_ranges
    Description :   Mapping input value from range to another range the relation is linear equation.
    Return      :   The mapped value after changing range of input to range of output.
    Arguments   :   - input_value:      value to be modified based on ranges.
                :    - input_range_min:  value of the minimum of input range.
                :    - input_range_max:  value of the maximum of input range.
                :    - output_range_min: value of the minimum of output range.
                :    - output_range_max: value of the maximum of output range.
    """
    return (input_value - input_range_min) * (output_range_max - output_range_min) / (
                input_range_max - input_range_min) + output_range_min;


def math_model(data=[[2, 0], [2, -70], [3, 80]], vehicle_length=4, direct_distance=4, theta=-50):
    """
        Name        :   math_model
        Description :   A method catch list of angels and distances and return list of direct distances,
                    :   The method applies this formula
                    :   Z = sqrt( (X)**2 + (Y)**2 -2(X)(Y)( cos gama ) )
                    :   X = x + L * sin(phi) / sin(gama)
                    :   Y = y + L * sin(theta) / sin(gama)
                    :   gama = 180 -theta - phi
        Return      :   The direct distances according to the passed values
        Arguments   :   - {data} list of 3 elements each element contains 2 values (distance and angle)
                    :   - {vehicle_length} the transmitter vehicle length
                    :   - {direct_distance} the distance between the sender and receiver.
                    :   - {theta} the angle between the sender and receiver.
    """
    absolute_distances = [-1, -1, -1]
    # data is list of 3 lists
    # each list have [car_distance, car_angle]

    if (None not in data) and (direct_distance > 0) and (60 <= theta <= 120) and (vehicle_length > 0):
        relatives = [relative_dist[0] for relative_dist in data]

        phis = [angle[1] for angle in data]

        # alphas = [ (90- abs(theta) + (90-abs(phi)) ) for phi in phis]
        alphas = [0] * 3
        # Tested for 9 cases of angels
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

        for i in range(0, 3):
            # Case 1, 4, 8, 9
            if (phis[i] > 0 and theta >= 0) or (phis[i] < 0 and theta <= 0):
                alphas[i] = 180 - abs(phis[i]) + abs(theta)

            # Case 2, 3
            elif (phis[i] < 0 and theta > 0) or (phis[i] > 0 and theta < 0):
                alphas[i] = 180 - (abs(phis[i]) + abs(theta))

            # Case 5
            elif phis[i] == 0 and theta == 0:
                alphas[i] = 180

            # Case 6, 7
            elif (phis[i] == 0) and (theta >= 0 or theta < 0):
                alphas[i] = 180 - abs(theta)

        # Tested over values
        b_lengths = [vehicle_length * abs(sin(radians(phis[i]))) / abs(sin(radians(alphas[i]))) for i in range(0, 3)]
        a_lengths = [vehicle_length * abs(sin(radians(theta))) / abs(sin(radians(alphas[i]))) for i in range(0, 3)]

        # Tested
        total_length_x = [direct_distance + abs(b_lengths[i]) for i in range(0, 3)]
        total_length_y = [relatives[i] + abs(a_lengths[i]) for i in range(0, 3)]

        # Tested
        absolute_distances = [round(sqrt(
            total_length_x[i] ** 2 + total_length_y[i] ** 2 - 2 * total_length_x[i] * total_length_y[i] * cos(
                radians(alphas[i]))), 4) for i in range(3)]

    return absolute_distances


def frame_to_positions(row_data=[[100, 100, 960, 540], [150, 150, 640, 360], [200, 200, 192, 108]],
                       frame_size=[1920, 1080], mode="FRONT"):
    """
    Name        :   frame_to_positions
    Description :   A method for calculate the angle of the objects in front of the main vehicle.
    Return      :   {position_angles} list of 3 elements represents the angle of the corresponding object.
    Arguments   :   -   {row_data} List of 3 elements each one contains 4 values x1, x2, y1, y2 borders of the object in frame.
                :   -   {frame_size} frame size.

"""
    if mode == "FRONT":
        # row_data is a list of 3 lists
        # Each list consist of starting_width, starting_height, width, height
        # Frame_size represents the resolution of camera which is used to capture the frame
        # For each center ( (x+width/2) , (y+height/2) )
        centers = [[(row_data[i][0] + (row_data[i][2] / 2)), (row_data[i][1] + (row_data[i][3] / 2))]
                   for i in range(0, 3)]
        # For get positions in relation of screen resolution
        print(f"Centers: {centers}")

    elif mode == "BACK":
        # For each center ( (x+width/2) , (y+height/2) )
        center = [[(row_data[0] + (row_data[2] / 2)), (row_data[1] + (row_data[3] / 2))]]
        # For get positions in relation of screen resolution
        print(f"Center: {center}")

    position_angels = [
        map_values_ranges(input_value=c[0], input_range_min=0, input_range_max=frame_size[0], output_range_min=0,
                          output_range_max=180) for c in center]

    print(f"Angels: {position_angels}")
    return position_angels

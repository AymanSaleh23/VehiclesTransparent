import threading
import time

from cv_algorithm.multi_cars_detection import ComputerVisionFrontal

# First Thread to run run_front in  ComputerVisionFrontal which contains while loop
from front_app.cv_global_variables import CVGlobalVariables

computer_vision_frontal_instance = ComputerVisionFrontal()  # instance for run ComputerVisionFrontal class
run_front = computer_vision_frontal_instance.run_front  # reference for run_front function without calling it

t1 = threading.Thread(target=run_front, args=[])
t1.start()

counter = 0
while True:
    counter = counter + 1
    result = CVGlobalVariables.detected_cars_centers_list
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Any Other app!!! : ", counter, result, '\n')
    time.sleep(0.5)

from threading import Thread
import time
from comlib.com_socket import *
from cv_algorithm.back_computer_vision_app import ComputerVisionBackApp
# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *
from mathematics.mathlib import *

received_frames_sock = Client("192.168.1.11", 20070, timeout=0.1)

# instance for run ComputerVisionFrontal class
computer_vision_back_instance = None
received_frame = None
received_discrete = None
received_fd = DataHolder()
direct_distance = None

if __name__ == "__main__":
    '''
    - Create CV object.
    - Create one measurement unit.
    - run Cv_obj.run_back() in thread.
    - receive frame, discrete from Cv_obj's sockets (applied internally in CV_back_app)
    - read single distance
    - pass all parameters to mathematical model 
    
    '''

    servo_obj = Angles(servo_pin=11)
    us_obj = Measure(trig=22, echo=23)

    computer_vision_back_instance = ComputerVisionBackApp(width=500, height=300)

    # CV model run front in thread
    t_cv_back = Thread(target=computer_vision_back_instance.run_back, args=[], daemon=True)
    t_cv_back.start()

    while True:
        received_frame, received_discrete = received_frames_sock.receive_all(1024)
        if received_frame is not None:
            # Update frames which is received from socket.
            computer_vision_back_instance.current_streamed_frame = received_frame
            received_fd.set_frame(received_frame)

        if received_discrete is not None:
            received_fd.set_discrete(received_discrete)

        if type(computer_vision_back_instance.front_vehicle_center) is list:
            direct_distance = us_obj.distance_read()
            abs_dist = math_model(data=received_fd.get_discrete()[0],
                                  vehicle_length=received_fd.get_discrete()[1],
                                  direct_distance=direct_distance,
                                  theta=computer_vision_back_instance.front_vehicle_center[0])
            print(f"Front Vehicle Center: {computer_vision_back_instance.front_vehicle_center[0]}")
            print(f"Absolute Distances: {abs_dist}")

        print(f"received_fd.get_discrete(): {received_fd.get_discrete()}")
        print(f'Data: \n{received_fd.get_discrete()}')
        time.sleep(0.01)
        received_fd.reset_discrete()

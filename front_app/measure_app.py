# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *

from comlib.com_socket import *
from threading import Thread

if __name__ == "__main__":
    """
    - Create Socket for measurement (inner socket)
    - Create Socket for send discrete (outer socket)
    - Create Angle, US objects.
    - run send discrete socket in thread
    """
    current_v_length = 5
    in_cv2measure_sock_angle = Client(ip="127.0.0.1", port=10051)
    out_sock_disc = Server(ip="192.168.1.11", port=10052)

    servo_obj_list = [Angles(servo_pin=11), Angles(servo_pin=12), Angles(servo_pin=13)]
    us_obj_list = [Measure(trig=22, echo=23), Measure(trig=24, echo=25), Measure(trig=26, echo=27)]

    dist_list = [0]*3
    cv_angle_list = last_angle_values = [0]*3

    t_send_disc = Thread(target=out_sock_disc.send, args=[])
    t_send_disc.setDaemon(True)
    t_send_disc.start()

    while True:
        time.sleep(0.3)
        try:
            cv_angle_list = in_cv2measure_sock_angle.recv_discrete()
        except Exception:
            cv_angle_list = [45, 90, 135]
        # Check if the last received values is different
        for section in range(0, len(servo_obj_list)):
            servo_obj_list[section].set_angle(cv_angle_list[section])
            dist_list[section] = us_obj_list[section].distance_read()
        last_angle_values = cv_angle_list
        to_send_dist_angl = [[d, a] for d in dist_list for a in cv_angle_list]
        out_sock_disc.update_to_send([to_send_dist_angl, current_v_length])
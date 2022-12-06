import threading
import time
from threading import Thread
from comlib import com_init_ip, com_socket
from cv_algorithm import detection_tracking

#To be tested on RPi
from distances import dist_angle, dist_measure

from mathematics import mathlib

PARAMETERS = {
    "FRAME_WIDTH": 750,
    "FRAME_HEIGHT": 500,
    "FRAME_TIMER_LIMIT": 30,
    "HOST_IP": "192.168.1.11",
    "SOCKET_FRAME_PORT": 50550,
    "SOCKET_DISCRETE_PORT": 50600,
    "SERVO_LEFT_PIN": 1,
    "SERVO_MEDDLE_PIN": 2,
    "SERVO_RIGHT_PIN": 3,
    "US_LEFT_TRIG_PIN": 4,
    "US_LEFT_ECHO_PIN": 5,
    "US_MEDDLE_TRIG_PIN": 6,
    "US_MEDDLE_ECHO_PIN": 7,
    "US_RIGHT_TRIG_PIN": 8,
    "US_RIGHT_ECHO_PIN": 9,
    "VEHICLE_LENGTH": 3,
    "VEHICLE_HEIGHT": 2
}
from comlib import com_socket

if __name__ == '__main__':
    #   Enable Computer vision feature to detect any vehicle
    computer_vision_object = detection_tracking.ComputerVisionAPP()

    #   Make {computer_vision_object} run in thread by Daemon
    vision_thread = threading.Thread( target= computer_vision_object.run_algorithm, args=[PARAMETERS["FRAME_WIDTH"], PARAMETERS["FRAME_HEIGHT"], PARAMETERS["FRAME_TIMER_LIMIT"]])
    vision_thread.setDaemon(True)

    #   Enable {vision_thread} to start its operations
    vision_thread.start()

    #   Initiate communication sockets for send {frame} and {discrete_data}
    server_socket_frames = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_FRAME_PORT"])
    server_socket_discrete_data = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_DISCRETE_PORT"])

    #   Set callback functions for sockets {server_socket_frames}, {server_socket_discrete_data}
    thread_socket_frame = threading.Thread(target=server_socket_frames)
    thread_socket_discrete_data = threading.Thread(target= server_socket_discrete_data)

    #   Enable Daemon for sockets {server_socket_frames}, {server_socket_discrete_data}
    thread_socket_frame.setDaemon(True)
    thread_socket_discrete_data.setDaemon(True)

    # Initiate {servo} objects and pass pins to them
    servo_left = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_LEFT_PIN"])
    servo_meddle = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_MEDDLE_PIN"])
    servo_right = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_RIGHT_PIN"])

    # Initiate {ultrasonic} objects and pass pins to them
    ultrasonic_left = dist_measure.Measure(PARAMETERS["US_LEFT_TRIG_PIN"],PARAMETERS["US_LEFT_ECHO_PIN"])
    ultrasonic_meddle = dist_measure.Measure(PARAMETERS["US_MEDDLE_TRIG_PIN"],PARAMETERS["US_MEDDLE_ECHO_PIN"])
    ultrasonic_right = dist_measure.Measure(PARAMETERS["US_RIGHT_TRIG_PIN"],PARAMETERS["US_RIGHT_ECHO_PIN"])

    # Initiate {servos} to be a list of {servo} objects to be easy to access
    servos = [servo_left, servo_meddle, servo_right]

    # Initiate {ultrasonics} to be a list of {ultrasonic} objects to be easy to access
    ultrasonics = [ultrasonic_left, ultrasonic_meddle, ultrasonic_right]

    #   Declaration of {reads} holds the data from {ultrasonic} readings, Initially clear it
    reads = [0]*3

    #   Enable sockets {server_socket_frames}, {server_socket_discrete_data} to start their job
    thread_socket_frame.start()
    thread_socket_discrete_data.start()

    #   Format of this data is list consist of list of 3 lists and the current vehicle length
    #   each sublist consist of 2 elements distance, angle
    #   Example  : data =  [ [[2,0],[2,-70],[3,80]], 4  ]
    discrete_data_to_send = [0,0]

    #   Declaration of variable {frame_to_send} to hold frames from {computer_vision_object} to be sent by {server_socket_frames}
    frame_to_send = [0]

    while True:
        #   Orient the US to the corresponding angles in format of list of 3 elements [a,b,c]
        for i in range(0,3):
            #   {computer_vision_object.data[i]} is updated in the {vision_thread}
            servos[i].set_angle(computer_vision_object.data[i])

        #   Enable Ultrasonics to read the distances
        reads = [ultrasonics[i].distance_read() for i in range(0, 3)]
        #   Construct the data to be sent using discrete socket
        discrete_data_to_send = [[reads[i], computer_vision_object.data[i]] for i in range(0, 3)].append(PARAMETERS["VEHICLE_LENGTH"])

        #   Update data to be sent in sockets in background
        server_socket_discrete_data.to_send = discrete_data_to_send
        server_socket_frames.to_send = frame_to_send
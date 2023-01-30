import threading, time
from comlib import com_init_ip, com_socket
from cv_algorithm import detection_tracking

# To be tested on RPi
from distances import dist_angle, dist_measure

from mathematics import mathlib

PARAMETERS = {
    "FRAME_WIDTH": 750,
    "FRAME_HEIGHT": 500,
    "FRAME_TIMER_LIMIT": 30,
    "HOST_IP": "127.0.0.1",
    "SOCKET_FRAME_PORT": 50550,
    "SOCKET_DISCRETE_PORT": 50600,
    "SERVO_LEFT_PIN": 7,
    "SERVO_MEDDLE_PIN": 11,
    "SERVO_RIGHT_PIN": 12,
    "US_LEFT_TRIG_PIN": 4,
    "US_LEFT_ECHO_PIN": 5,
    "US_MEDDLE_TRIG_PIN": 6,
    "US_MEDDLE_ECHO_PIN": 7,
    "US_RIGHT_TRIG_PIN": 8,
    "US_RIGHT_ECHO_PIN": 9,
    "VEHICLE_LENGTH": 3,
    "VEHICLE_HEIGHT": 2,
    "LEFT": 0,
    "MEDDLE": 1,
    "RIGHT": 2
}

#   Declaration of global variables
server_socket_frames = 0
server_socket_discrete_data = 0
computer_vision_object = 0
ultrasonic_left = 0
ultrasonic_meddle = 0
ultrasonic_right = 0
servo_left = 0
servo_meddle = 0
servo_right = 0


def synch_send_frame():
    """ To implement the logic sending the frame from the computer vision model to be sent by {server_socket_frames} """
    #   Declaration of variable {frame_to_send}
    #   Tto hold frames from {computer_vision_object} to be sent by {server_socket_frames}
    while True:
        frame_to_send = computer_vision_object.frame_pure
        server_socket_frames.update_to_send(frame_to_send)


def synch_send_discrete_data(discrete_data):
    """ To implement the logic for sending the discrete data which is fetched before """
    server_socket_discrete_data.update_to_send(discrete_data)


def fetch_discrete_data():
    """ To implement the logic for fetching discrete data Distance (Ultrasonic, Servo)"""
    # Initiate {servos} to be a list of {servo} objects to be easy to access
    servos = [servo_left, servo_meddle, servo_right]

    # Initiate {ultrasonics} to be a list of {ultrasonic} objects to be easy to access
    ultrasonics = [ultrasonic_left, ultrasonic_meddle, ultrasonic_right]

    #   Declaration of {reads} holds the data from {ultrasonic} readings, Initially clear it
    read_distances = [0] * 3

    # Continue fetching forever
    while True:
        # Update {row_angels_data} field from the computer vision model which is updated continuously.
        row_angels_data = computer_vision_object.data

        # Orient Servos
        servo_left.set_angle(row_angels_data[0])
        servo_meddle.set_angle(row_angels_data[1])
        servo_right.set_angle(row_angels_data[2])

        # Fetch distances by US
        read_distances[0] = ultrasonic_left.distance_read()
        read_distances[1] = ultrasonic_meddle.distance_read()
        read_distances[2] = ultrasonic_right.distance_read()

        #   Format of this data is list consist of list of 3 lists and the current vehicle length
        #   each sublist consist of 2 elements distance, angle
        #   Example  : data =  [ [[2,0],[2,-70],[3,80]], 4  ]
        discrete_data_to_send = [[read_distances[i], row_angels_data[i]]
                                 for i in range(0, 3)].append(PARAMETERS["VEHICLE_LENGTH"])

        #   Send to its socket {server_socket_discrete_data} to be transmitted
        synch_send_discrete_data(discrete_data_to_send)


if __name__ == '__main__':
    """ For initialization of global variables (Servos, US, CV) and,
    Creating Threads of all project functions and runs it."""

    #   Initiate communication sockets for send {frame} and {discrete_data}.
    server_socket_frames = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_FRAME_PORT"])
    server_socket_discrete_data = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_DISCRETE_PORT"])

    #   Enable Computer vision feature to detect any vehicle.
    computer_vision_object = detection_tracking.ComputerVisionAPP()

    # Initiate {ultrasonic} objects and pass pins to them.
    ultrasonic_left = dist_measure.Measure(PARAMETERS["US_LEFT_TRIG_PIN"], PARAMETERS["US_LEFT_ECHO_PIN"])
    ultrasonic_meddle = dist_measure.Measure(PARAMETERS["US_MEDDLE_TRIG_PIN"], PARAMETERS["US_MEDDLE_ECHO_PIN"])
    ultrasonic_right = dist_measure.Measure(PARAMETERS["US_RIGHT_TRIG_PIN"], PARAMETERS["US_RIGHT_ECHO_PIN"])

    # Initiate {servo} objects and pass pins to them
    servo_left = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_LEFT_PIN"])
    servo_meddle = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_MEDDLE_PIN"])
    servo_right = dist_angle.Angles(servo_pin=PARAMETERS["SERVO_RIGHT_PIN"])

    #   Set callback functions for sockets {server_socket_frames}, {server_socket_discrete_data}
    thread_socket_frame = threading.Thread(target=server_socket_frames.send)
    thread_socket_discrete_data = threading.Thread(target=server_socket_discrete_data.send)

    thread_vision = threading.Thread(target=computer_vision_object.run_algorithm,
                                     args=[PARAMETERS["FRAME_WIDTH"],
                                           PARAMETERS["FRAME_HEIGHT"],
                                           PARAMETERS["FRAME_TIMER_LIMIT"]])

    #   Thread for fetching discrete data from the socket
    thread_fetch_discrete_data = threading.Thread(target=fetch_discrete_data)

    #   Tread to update frame to be sent synchronously
    thread_fetch_frame = threading.Thread(target=synch_send_frame)

    #   Make {computer_vision_object} run in thread by Daemon
    thread_vision.setDaemon(True)
    #   Enable Daemon for sockets {server_socket_frames}, {server_socket_discrete_data}, {fetch_discrete_data}
    thread_socket_frame.setDaemon(True)
    thread_socket_discrete_data.setDaemon(True)
    thread_fetch_discrete_data.setDaemon(True)
    thread_fetch_frame.setDaemon(True)

    #   Enable {vision_thread} to start its operations
    thread_vision.start()
    #   Enable sockets {server_socket_frames}, {server_socket_discrete_data} to start their job
    thread_socket_frame.start()
    thread_socket_discrete_data.start()
    thread_fetch_discrete_data.start()
    thread_fetch_frame.start()

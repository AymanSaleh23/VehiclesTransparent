import threading, time
from comlib import com_init_ip, com_socket
from cv_algorithm import detection_tracking

#To be tested on RPi
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
    "VEHICLE_HEIGHT": 2
}

if __name__ == '__main__':
    #>>>   Enable Computer vision feature to detect any vehicle (Algorithm is run in main)
    computer_vision_object = detection_tracking.ComputerVisionAPP()

    #   Make {computer_vision_object} run in thread by Daemon
    vision_thread = threading.Thread(target=computer_vision_object.run_algorithm, args=[PARAMETERS["FRAME_WIDTH"], PARAMETERS["FRAME_HEIGHT"], PARAMETERS["FRAME_TIMER_LIMIT"]])
    vision_thread.setDaemon(True)

    #   Enable {vision_thread} to start its operations
    vision_thread.start()

    #   Initiate communication sockets for send {frame} and {discrete_data}
    server_socket_frames = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_FRAME_PORT"])
    server_socket_discrete_data = com_socket.Server(ip=PARAMETERS["HOST_IP"], port=PARAMETERS["SOCKET_DISCRETE_PORT"])

    #   Set callback functions for sockets {server_socket_frames}, {server_socket_discrete_data}
    thread_socket_frame = threading.Thread(target=server_socket_frames)
    thread_socket_discrete_data = threading.Thread(target=server_socket_discrete_data)

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
    discrete_data_to_send = [None, None]

    #   Declaration of variable {frame_to_send}
    #   Tto hold frames from {computer_vision_object} to be sent by {server_socket_frames}
    frame_to_send = [None]

    while True:

        # Detection And Tracking Instances
        od = ObjectDetection()
        ot = ObjectTracking()

        # Initialize The x1,y1,x2,y2,text,conf,bbox
        x1, y1, x2, y2, text, conf, bbox = 0, 0, 0, 0, '', 0, 0

        # Read video
        video = cv2.VideoCapture("video2.mp4")

        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        # Flag To Run Detection After 25 Frame
        periodic_timer = 0
        # Flag To Run Detection For The First Frame
        isFirstFrame = True

        while True:
            # read Frame by frame
            ok, frame = video.read()
            # Resize the Frame
            frame = cv2.resize(frame, (width, height))

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                sys.exit()
                break

            # Detect the Car at the first frame only
            if (isFirstFrame):
                x1, y1, x2, y2, text, conf = od.detect(frame)
                if (conf != 0):
                    w = abs(x1 - x2)
                    h = abs(y1 - y2)
                    # Define an initial bounding box
                    bbox = (x1, y1, w, h)
                    ok = ot.track_init(frame, bbox)
                    print('############ GET The First Car ##################')
                    print('BBOX : ', bbox)
                    print('#########################################')
                periodic_timer = 0
                isFirstFrame = False
                print('*********************** First Frame Detection **************************')

            else:
                if (periodic_timer % timer_limit == 0 or conf == 0):
                    x1, y1, x2, y2, text, conf = od.detect(frame)
                    if (conf != 0):
                        w = abs(x1 - x2)
                        h = abs(y1 - y2)
                        bbox = (x1, y1, w, h)  # Define an initial bounding box
                        ok = ot.track_init(frame, bbox)
                        print('############### GET A Car After Timer ##############')
                        print('BBOX : ', bbox)
                        print('####################################################')

                    if (periodic_timer % timer_limit == 0):
                        periodic_timer = 0
                    print('*********************** Repeat Detection **************************')

            periodic_timer = periodic_timer + 1  # Counter The Period_counter Flag

            print('******** TIME : ', periodic_timer, ' ***********')

            # No detected Cars 'conf = 0 '
            if (conf == 0):
                cv2.putText(frame, "No Detected Cars OR Holding After Timer period ", (23, 23),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            else:
                # Start Trackng
                # Start timer
                timer = cv2.getTickCount()

                # Update tracker
                ok, bbox = ot.update_track(frame)

                # Calculate Frames per second (FPS)
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

                if ok:
                    # Tracking success
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    self.frame_pure = frame
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 3)
                    print('################### GET A Car  #####################')
                    print('BBOX : ', bbox)
                    print('####################################################')
                else:
                    print('++++++++++++++++ Tracking Failed +++++++++++++++++')
                # End Traking

                print("===================")
                print("Data :  x1: ", x1, ' , y1: ', y1, ' , x2: ', x2, ' , y2: ', y2, ' , text_conf: ', text)
                print("===================")

                #   Create variable holds the angels from the model
                row_data = [[0], [0], [0], [0]] * 3
                # Update data field which is read asynchronously
                #   >>> Pass the front vehicles' data (positions) initially all have the same data
                row_data = mathlib.frame_to_positions(
                    row_data=[[bbox[0], bbox[1], bbox[2], bbox[3]], [bbox[0], bbox[1], bbox[2], bbox[3]],
                              [bbox[0], bbox[1], bbox[2], bbox[3]]], frame_size=[width, height])

                #   Orient the US to the corresponding angles in format of list of 3 elements [a,b,c]
                for i in range(0, 3):
                    #   {row_data[i]} is updated
                    servos[i].set_angle(row_data[i])

                    #   Enable Ultrasonics to read the distances
                    reads = [ultrasonics[i].distance_read() for i in range(0, 3)]

                    #   Construct the data to be sent using socket {server_socket_discrete_data}
                    discrete_data_to_send = [[reads[i], reads[i]] for i in range(0, 3)].append(
                        PARAMETERS["VEHICLE_LENGTH"])
                print("===================")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
            x1, y1, x2, y2, text = 0, 0, 0, 0, ''
            cv2.putText(frame, "{} {}".format("Frame NO : ", periodic_timer), (23, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 255), 2)
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (23, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
            cv2.imshow('Frame', frame)
            #     cv2.waitKey(0)
            # Exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):  # if press SPACE
                break
        video.release()
        cv2.destroyAllWindows()

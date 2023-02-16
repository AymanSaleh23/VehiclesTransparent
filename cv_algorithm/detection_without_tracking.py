"""
This is just run function
Detection without tracking for back car
"""

def run():
    # Some Initial  Parameters
    width, height = 1000,700  # ReSize the Frame
    x1,y1,x2,y2,text,conf,area,bbox,fps = 0,0,0,0,'',0,0,0,0 # Initialize The x1,y1,x2,y2,text,conf,bbox
    streamedData  = None
    C_X,C_Y,tolerance =  int(width/2), int(height/2),120  # Selecting the center for ROI 'region of interest',and its left and right distance.

    # Detection And Tracking Instances
    od = SingleCardetection()
    
    video = cv2.VideoCapture("video2.mp4") # Read video
    S_video = cv2.VideoCapture("video2.mp4") # Read Straemed video
    logo = cv2.imread('Valeo.png')
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    if not S_video.isOpened():
        print('Could not Open Streamed Video')
    while True:
        ok,frame = video.read()    #read Frame by frame
        frame= cv2.resize(frame, (width, height))  # Resize the Frame
        
        S_ok , S_frame = S_video.read()   # read recived Video


        # Exit if video not opened.
        if not ok:
            print ('Cannot read video file')
            sys.exit()
            break
        
        # Replace The StreamedData with Streamed Frame if its not None else make it take logo Image
        if not S_ok:
            print ('Cannot read Streamed video file')
            streamedData = logo
        else:
            streamedData = S_frame
        
        

        if ok:  
            timer = cv2.getTickCount()   # Start timer To Calculate FPS
        
            # Adjust ROI 'Region of interest'
            cv2.rectangle(frame,(C_X-tolerance,C_Y), (C_X+tolerance,height), (255,255,255),1) # ROI bounding Box
            cv2.circle(frame, (C_X,C_Y), radius=0, color=(0, 0, 255), thickness=3)            # ROI Center Point
            ROI_Frame = frame[C_Y:height,C_X-tolerance:C_X+tolerance]  # To Make the detection and tracking Only for The ROI instead of the whole frame.

            x1,y1,x2,y2,text,conf,area = od.detect(ROI_Frame) # detecting a car in ROI   
            detected_car_width = round(abs(x2-x1))
            detected_car_height = round(abs(y2-y1))
            #Fill Streamed Video
            if area != 0:
                streamedData = cv2.resize(streamedData, (detected_car_width, detected_car_height))
                ROI_Frame[y1: y2 ,x1: x2] = cv2.addWeighted(ROI_Frame[y1: y2 ,x1: x2],0.4,streamedData,0.6,0) 

            
            cv2.rectangle(ROI_Frame, (x1, y1), (x2, y2), (0, 255,255), 1)
            x1,y1,x2,y2,text,area = 0,0,0,0,'',0
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);  # Calculate Frames per second (FPS)
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (23,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,255,255), 2);
            cv2.imshow('Frame' , frame)
#         cv2.waitKey(0)
        else:
            sys.exit()
        if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE 
            break

    video.release()
    cv2.destroyAllWindows()




    run()
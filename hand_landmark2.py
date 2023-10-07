import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import datetime
import csv

import pyzed.sl as sl

MODE = 'zed' # 'zed' or 'webcam'

# media pipe setting
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

file_duration = 10
header_csv = ["Left_Wrist_x", "Left_Wrist_y", "Left_Wrist_z", 
            "Left_Thumb_cmc_x", "Left_Thumb_cmc_y", "Left_Thumb_cmc_z",
            "Left_Thumb_mcp_x", "Left_Thumb_mcp_y", "Left_Thumb_mcp_z",
            "Left_Thumb_ip_x", "Left_Thumb_ip_y", "Left_Thumb_ip_z",
            "Left_Thumb_tip_x", "Left_Thumb_tip_y", "Left_Thumb_tip_z",
            "Left_Index_finger_mcp_x", "Left_Index_finger_mcp_y", "Left_Index_finger_mcp_z",
            "Left_Index_finger_pip_x", "Left_Index_finger_pip_y", "Left_Index_finger_pip_z",
            "Left_Index_finger_dip_x", "Left_Index_finger_dip_y", "Left_Index_finger_dip_z",
            "Left_Index_finger_tip_x", "Left_Index_finger_tip_y", "Left_Index_finger_tip_z",
            "Left_Middle_finger_mcp_x", "Left_Middle_finger_mcp_y", "Left_Middle_finger_mcp_z",
            "Left_Middle_finger_pip_x", "Left_Middle_finger_pip_y", "Left_Middle_finger_pip_z", 
            "Left_Middle_finger_dip_x", "Left_Middle_finger_dip_y", "Left_Middle_finger_dip_z",
            "Left_Middle_finger_tip_x", "Left_Middle_finger_tip_y", "Left_Middle_finger_tip_z",
            "Left_Ring_finger_mcp_x", "Left_Ring_finger_mcp_y", "Left_Ring_finger_mcp_z",
            "Left_Ring_finger_pip_x", "Left_Ring_finger_pip_y", "Left_Ring_finger_pip_z",
            "Left_Ring_finger_dip_x", "Left_Ring_finger_dip_y", "Left_Ring_finger_dip_z",
            "Left_Ring_finger_tip_x", "Left_Ring_finger_tip_y", "Left_Ring_finger_tip_z",
            "Left_Pinky_mcp_x", "Left_Pinky_mcp_y", "Left_Pinky_mcp_z",
            "Left_Pinky_pip_x", "Left_Pinky_pip_y", "Left_Pinky_pip_z",
            "Left_Pinky_dip_x", "Left_Pinky_dip_y", "Left_Pinky_dip_z",
            "Left_Pinky_tip_x", "Left_Pinky_tip_y", "Left_Pinky_tip_z",
            "Right_Wrist_x", "Right_Wrist_y", "Right_Wrist_z",
            "Right_Thumb_cmc_x", "Right_Thumb_cmc_y", "Right_Thumb_cmc_z",
            "Right_Thumb_mcp_x", "Right_Thumb_mcp_y", "Right_Thumb_mcp_z",
            "Right_Thumb_ip_x", "Right_Thumb_ip_y", "Right_Thumb_ip_z",
            "Right_Thumb_tip_x", "Right_Thumb_tip_y", "Right_Thumb_tip_z",
            "Right_Index_finger_mcp_x", "Right_Index_finger_mcp_y", "Right_Index_finger_mcp_z",
            "Right_Index_finger_pip_x", "Right_Index_finger_pip_y", "Right_Index_finger_pip_z",
            "Right_Index_finger_dip_x", "Right_Index_finger_dip_y", "Right_Index_finger_dip_z",
            "Right_Index_finger_tip_x", "Right_Index_finger_tip_y", "Right_Index_finger_tip_z",
            "Right_Middle_finger_mcp_x", "Right_Middle_finger_mcp_y", "Right_Middle_finger_mcp_z",
            "Right_Middle_finger_pip_x", "Right_Middle_finger_pip_y", "Right_Middle_finger_pip_z",
            "Right_Middle_finger_dip_x", "Right_Middle_finger_dip_y", "Right_Middle_finger_dip_z",
            "Right_Middle_finger_tip_x", "Right_Middle_finger_tip_y", "Right_Middle_finger_tip_z",
            "Right_Ring_finger_mcp_x", "Right_Ring_finger_mcp_y", "Right_Ring_finger_mcp_z",
            "Right_Ring_finger_pip_x", "Right_Ring_finger_pip_y", "Right_Ring_finger_pip_z",
            "Right_Ring_finger_dip_x", "Right_Ring_finger_dip_y", "Right_Ring_finger_dip_z",
            "Right_Ring_finger_tip_x", "Right_Ring_finger_tip_y", "Right_Ring_finger_tip_z",
            "Right_Pinky_mcp_x", "Right_Pinky_mcp_y", "Right_Pinky_mcp_z",
            "Right_Pinky_pip_x", "Right_Pinky_pip_y", "Right_Pinky_pip_z",
            "Right_Pinky_dip_x", "Right_Pinky_dip_y", "Right_Pinky_dip_z",
            "Right_Pinky_tip_x", "Right_Pinky_tip_y", "Right_Pinky_tip_z",
            "timestamp"]


curr_timestamp = datetime.datetime.now().timestamp()
start_time = datetime.datetime.now()
csvfile = open(f'sample_{curr_timestamp}.csv', 'w')
writer = csv.writer(csvfile) 
writer.writerow(header_csv)


# Create a Camera object
if MODE == 'zed':
    zed = sl.Camera()
    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD1080 video mode
    init_params.camera_fps = 30  # Set fps at 30
    
    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()
        
    # Capture frames and stop
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    
elif MODE == 'webcam':
    cap = cv2.VideoCapture(0)
    
key_wait = 10

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while True:
        # Create the first empty value
        sensor_reading = [0.0 for i in range(127)]
        # Grab an image, a RuntimeParameters object must be given to grab()
        if MODE=='zed':
            no_error = True if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS else False
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT).get_milliseconds()  # Get the timestamp at the time the image was captured
            ## Get the image ##
            image_left_ocv = image.get_data()
            
        elif MODE=='webcam':
            no_error = True if cap.isOpened()==True else False
            ret, image_left_ocv = cap.read()
            timestamp = datetime.datetime.now().timestamp()
        
        if no_error:
            
            ## Detect the hand ##
            # Recolor Feed
            image_left_ocv = cv2.cvtColor(image_left_ocv, cv2.COLOR_BGR2RGB)
            
            # Flip on horizontal, as stated by the website the picture is inverted
            image_left_ocv = cv2.flip(image_left_ocv, 1)
            # Set flag
            image_left_ocv.flags.writeable = False # locks the image
            # Make Detections
            results = hands.process(image_left_ocv)
            # Set flag to true
            image_left_ocv.flags.writeable = True
            
            
            ## Show the image ##
            # draw landmark
            image_left_ocv = cv2.cvtColor(image_left_ocv, cv2.COLOR_RGB2BGR)
            clean_image = image_left_ocv.copy()
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image_left_ocv, hand, mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
                ## Save record ##
                # record timestamp
                sensor_reading[126] = timestamp
                for num_hands in range(len(results.multi_hand_landmarks)):
                    # case when only right hand is detected
                    if results.multi_handedness[num_hands].classification[0].label == 'Right':
                        for index,data_point in enumerate(results.multi_hand_world_landmarks[num_hands].landmark):
                            print(index)
                            sensor_reading[index*3+63] = data_point.x
                            sensor_reading[index*3+64] = data_point.y
                            sensor_reading[index*3+65] = data_point.z
                    elif results.multi_handedness[num_hands].classification[0].label == 'Left':
                        for index,data_point in enumerate(results.multi_hand_world_landmarks[num_hands].landmark):
                            
                            sensor_reading[index*3] = data_point.x
                            sensor_reading[index*3+1] = data_point.y
                            sensor_reading[index*3+2] = data_point.z
                
                elapsed_time = (datetime.datetime.now() - start_time).seconds
                if elapsed_time >= file_duration:
                    csvfile.close()
                    curr_timestamp = datetime.datetime.now().timestamp()
                    csvfile = open(f'sample_{curr_timestamp}.csv', 'w')
                    writer = csv.writer(csvfile)

                    # Write headers to the new CSV file)
                    writer.writerow(header_csv)

                    start_time = datetime.datetime.now()
                
                writer.writerow(sensor_reading)
                
            # display image with timestamp
            cv2.putText(clean_image, str(timestamp), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
            
            # concat image
            numpy_horizontal = np.hstack((image_left_ocv, clean_image))
            numpy_horizontal_concat = np.concatenate((image_left_ocv, clean_image), axis=1)

            cv2.imshow("ZED | 2D View", numpy_horizontal_concat)
            print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image_left_ocv.shape[1], image_left_ocv.shape[0],
                    timestamp))
            ## Interrupt command ##
            key = cv2.waitKey(key_wait)
            

            
            if key == 113: # for 'q' key
                print("Exiting...")
                break
            if key == 109: # for 'm' key
                if (key_wait>0):
                    print("Pause")
                    key_wait = 0 
                else : 
                    print("Restart")
                    key_wait = 10 
            if key == 99: # for 'c' key
                print('Capturing...')
                cv2.imwrite(os.path.join('{}.jpg'.format(uuid.uuid1())), image_left_ocv)

csvfile.close()
# Close the camera
if MODE=='zed':
    image.free(sl.MEM.CPU)
    zed.close()
cv2.destroyAllWindows()
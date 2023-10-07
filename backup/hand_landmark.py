import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

import pyzed.sl as sl

# media pipe setting
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Create a Camera object
zed = sl.Camera()

# Create a InitParameters object and set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
init_params.camera_fps = 30  # Set fps at 30

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Camera Open : "+repr(err)+". Exit program.")
    exit()

# Capture frames and stop
image = sl.Mat()
runtime_parameters = sl.RuntimeParameters()
key_wait = 10

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic: 
    while True:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
            
            ## Get the image ##
            image_left_ocv = image.get_data()
            
            ## Detect the hand ##
            # Recolor Feed
            image_left_ocv = cv2.cvtColor(image_left_ocv, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image_left_ocv)
            
            
            ## Show the image ##
            # draw landmark
            # Right hand
            mp_drawing.draw_landmarks(image_left_ocv, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                      )
            # Left Hand
            mp_drawing.draw_landmarks(image_left_ocv, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                      )
            # Pose Detections
            mp_drawing.draw_landmarks(image_left_ocv, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                      )
            # display
            image_left_ocv = cv2.cvtColor(image_left_ocv, cv2.COLOR_RGB2BGR)
            cv2.imshow("ZED | 2D View", image_left_ocv)
            print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(),
                    timestamp.get_milliseconds()))
            
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
                
# Close the camera
image.free(sl.MEM.CPU)
zed.close()
cv2.destroyAllWindows()
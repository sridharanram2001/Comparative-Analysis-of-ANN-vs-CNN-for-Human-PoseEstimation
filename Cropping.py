# Import required libraries

import cv2
import mediapipe as mp
import time
import numpy as np
import keyboard
import datetime

#Define MediaPipe Objects
mpDraw = mp.solutions.drawing_utils 
mpPose = mp.solutions.pose
pose = mpPose.Pose()


#Define VideoCapture object
cap = cv2.VideoCapture(0)


#Define pressing time and Key press object
pTime = 0
key = keyboard.read_key()



cx = [0 for x in range(33)]
cy = [0 for y in range(33)]


# Main

if key == 'z':                               # Wait for the key press "z"
    time.sleep(5)                             
    start_time = datetime.datetime.now()     # Record the starting time 
    i=503
    while True:
        success, img = cap.read()                       # Read the image from the video capture object   
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # Convert the image from BGR to RGB format
        results = pose.process(imgRGB)                  # Identiy the pose in the image using the pose object 
        image = np.zeros((480, 640, 3))

        if results.pose_landmarks:
            mpDraw.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # Draw the obtained pose keypoints
            for id, lm in enumerate(results.pose_landmarks.landmark):       
                h, w, c = img.shape
                print(h, w, c)
                print(id, lm)
                cx[id], cy[id] = int(lm.x * w), int(lm.y * h)     # Use the keypoints to draw a bounding box
                x_max = max(cx)                                  
                x_min = min(cx)
                y_max = max(cy)
                y_min = min(cy)
                roi = image[y_min-10:y_max+10, x_min-10:x_max+10]     # Crop the ROI
            path = f"D:\\Pycharm\\Anomalous_detection_CNN\\data_four_poses\\test\\normal\\Image{i}.png"
            cv2.imwrite(path, roi)     # Define the path and save the image
            i = i + 1

        later_time = datetime.datetime.now()           # Calculate for every loop
        difference = later_time - start_time           # Calcuale the difference between Start and End time 
        sec_diff = difference.total_seconds()          # Get the time in seconds 
        sec_diff = round(sec_diff)
        #print(sec_diff)
        #print("\n")
        if sec_diff == 2:                              # If the time reaches a certain set seconds the loop breaks    
            break

        cv2.imshow("Image", img)                       # Show the image in a window
        cv2.waitKey(80)
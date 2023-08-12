import cv2
import mediapipe as mp
import time
import math
import keyboard
import datetime

# create required objects for the MediaPipe library
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# initialize the camera
cap = cv2.VideoCapture(0)

# open a csv file to save the key points
f = open("test.csv","a")

# wait until a key is pressed
key = keyboard.read_key()

# if the pressed key is z then start collecting the key points
if key == 'z':
    time.sleep(8) # wait for few seconds before starting to collect the key points so that user can take the position
    start_time = datetime.datetime.now() # save the time of starting data collection
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        # print(results.pose_landmarks)
        lmList = [] # create an empty array every time
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # draw landmarks on the image
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(h,w,c)
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h) # compute the x, y coordinates of the key points based on the image shape
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED) # draw circles on top of key points. Can be used if needed.
                lmList.append([id + 1, cx, cy]) # append the key points to the empty list

        if lmList != []:
            # if the list is not empty store the list data in the CSV file
            print(lmList)
            f.write(str(lmList) + "\n")
        later_time = datetime.datetime.now()
        difference = later_time - start_time
        sec_diff = difference.total_seconds()
        sec_diff = round(sec_diff)
        #print(sec_diff)
        #print("\n")
        # if the sec_diff is 40 seconds, stop the data collection
        if sec_diff == 40:
            break


        cv2.imshow("Image", img)
        cv2.waitKey(10)
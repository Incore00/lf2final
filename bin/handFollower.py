import cv2
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 60)


while 1:
	_, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	cv2.imshow('Virtual Mouse', frame)
	cv2.waitKey(1)
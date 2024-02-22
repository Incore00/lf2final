import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
from datetime import datetime
import time
import pyautogui
from mediapipe.framework.formats import landmark_pb2
from math import sqrt

pyautogui.FAILSAFE = 0
pyautogui.PAUSE = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 30)
prev_frame_time = 0

sec_x = None
thumb_x = None

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, model_complexity=1) as hands:
	while cap.isOpened():
		new_frame_time = time.time()
		ret, frame = cap.read()
		frame_height, frame_width, _ = frame.shape
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image = cv2.flip(image, 1)
		results = hands.process(image)
		landmark_list = results.multi_hand_landmarks
		hand_type = results.multi_handedness
		right_hand_landmarks = []
		if landmark_list:
			for index, hand, landmarks_list in zip(range(0, len(hand_type)), hand_type, landmark_list):
				if 'Right' in str(hand):
					right_hand_landmarks.append(landmarks_list)
		if str(right_hand_landmarks) != "[]":
			for hand in right_hand_landmarks:
				mp_drawing.draw_landmarks(image, hand)
				landmarks = hand.landmark
				for id, landmark in enumerate(landmarks):
					x = int(landmark.x * 1920)
					y = int(landmark.y * 1080)
					if id == 8:
						#pyautogui.moveTo(-x + 3840, 1080 - y)
						pass
					#if id == 4:
					#	thumb_x = landmark.x * frame_width
					#	thumb_y = landmark.y * frame_height
					#if id == 5:
					#	sec_x = landmark.x * frame_width
					#	sec_y = landmark.y * frame_height
					#if thumb_x != None and sec_x != None:
					#	calc_x = thumb_x - sec_x
					#	calc_y = thumb_y - sec_y
					#	print(sqrt(calc_x*calc_x+calc_y*calc_y))
						#if sqrt(calc_x * calc_x + calc_y * calc_y) < 40:
						#	pyautogui.click(button='left')
						#	pyautogui.b

		fps = 1 / (new_frame_time - prev_frame_time)
		prev_frame_time = new_frame_time
		print('FPS:', int(fps))
		#cv2.imshow('Virtual Mouse', image)
		#cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()
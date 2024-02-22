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

class HandFollower():
	def __init__(self, queue):
		self.queue = queue

		pyautogui.FAILSAFE = 0
		pyautogui.PAUSE = 0

		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_hands = mp.solutions.hands

		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
		self.cap.set(cv2.CAP_PROP_FRAME_COUNT, 30)
		self.prev_frame_time = 0

		self.sec_x = None
		self.thumb_x = None

		self.run()

	def run(self):
		with self.mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3, model_complexity=0) as hands:
			while self.cap.isOpened():
				self.new_frame_time = time.time()
				ret, frame = self.cap.read()
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
						self.mp_drawing.draw_landmarks(image, hand)
						landmarks = hand.landmark
						for id, landmark in enumerate(landmarks):
							x = int(landmark.x * 1920)
							y = int(landmark.y * 1080)
							if id == 8:
								pyautogui.moveTo(x, -1080 + y)
								#u andrzeja dolna geometria
								# pyautogui.moveTo(-x + 3840, 1080 - y)
				fps = 1 / (self.new_frame_time - self.prev_frame_time)
				self.prev_frame_time = self.new_frame_time
				print('FPS:', int(fps))
				#cv2.imshow('Virtual Mouse', image)
				#cv2.waitKey(1)
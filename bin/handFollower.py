import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.python import solutions
from mediapipe.framework.formats import landmark_pb2
from math import sqrt
from datetime import datetime
from multiprocessing import Pool

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2, running_mode=2)
hand_detector = vision.HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 60)
drawing = solutions.drawing_utils
pyautogui.FAILSAFE = False


def task(frame):
	frame_height, frame_width, _ = frame.shape
	rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	prepared_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

	detection_result = hand_detector.detect(prepared_frame)
	hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
	hand_landmarks_list = detection_result.hand_landmarks
	sec_x = None
	thumb_x = None
	for index, hand, landmarks_list in zip(range(0, len(detection_result.handedness)), detection_result.handedness,
										   hand_landmarks_list):
		if 'Left' in str(hand):
			hand_landmarks_list.remove(landmarks_list)
	for idx in range(len(hand_landmarks_list)):
		hand_landmarks = hand_landmarks_list[idx]
		hand_landmarks_proto.landmark.extend(
			[landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
		drawing.draw_landmarks(frame, hand_landmarks_proto)
		landmarks = hand_landmarks_proto.landmark
		for id, landmark in enumerate(landmarks):
			x = landmark.x * frame_width
			y = landmark.y * frame_height
			# print(x,y)
			if id == 8:
				pyautogui.moveTo(x, -1080 + y)
			#if id == 4:
			#	thumb_x = landmark.x * frame_width
			#	thumb_y = landmark.y * frame_height
			#if id == 6:
			#	sec_x = landmark.x * frame_width
			#	sec_y = landmark.y * frame_height
			#if thumb_x != None and sec_x != None:
			#	calc_x = thumb_x - sec_x
			#	calc_y = thumb_y - sec_y
			#	# print(math.sqrt(calc_x*calc_x+calc_y*calc_y))
			#	if sqrt(calc_x * calc_x + calc_y * calc_y) < 40:
			#		pyautogui.click(button='left')

while 1:
	time1 = datetime.now()
	_, frame = cap.read()
	task(frame)
	print(datetime.now() - time1)
	cv2.imshow('Virtual Mouse', frame)
	cv2.waitKey(1)
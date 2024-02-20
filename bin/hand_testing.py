import cv2
from datetime import datetime
import mediapipe as mp
from multiprocessing import Process
import time

frame_list = []
processed_frame = []

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#cap.set(cv2.CAP_PROP_FRAME_COUNT, 60)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def data_creator():
	while 1:
		ret, frame = cap.read()
		frame_list.append(frame)
def hand_detector():
	while 1:
		if frame_list > 0:
			frame = frame_list.pop(0)
			image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image = cv2.flip(image, 1)
			image.flags.writeable = False
			results = hands.process(image)
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			if results.multi_hand_landmarks:
				for num, hand in enumerate(results.multi_hand_landmarks):
					mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
											  mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
											  mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),)
			processed_frame.append(image)

def show_data():
	while 1:
		print('frames to process:',len(frame_list), 'frames_processed',len(processed_frame))
		time1 = datetime.now()
		#hand_detector(frame_list.pop(0))
		cv2.imshow('Hand Tracking', processed_frame.pop(0))
		print(datetime.now() - time1)
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
if __name__ == '__main__':
	Process(target=data_creator).start()
	Process(target=hand_detector).start()
	time.sleep(5)
	Process(target=show_data).start()

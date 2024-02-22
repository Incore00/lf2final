import mediapipe as mp
import cv2
from datetime import datetime
import multiprocessing as mproc


def readFrames (raw_queue, proc_queue):
	cap = cv2.VideoCapture(0)
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			raw_queue.put(frame)
			try:
				proc_frame = proc_queue.get(0)
				cv2.imshow('Proc Frame', proc_frame)
			except:
				continue
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cap.release()
				cv2.destroyAllWindows()
				return -1
		else:
			return

class DetectorInstance():
	def __init__(self, raw_queue, proc_queue):
		super().__init__()

		self.raw_queue = raw_queue
		self.proc_queue = proc_queue

		self.mp_hands = mp.solutions.hands
		self.mp_drawing = mp.solutions.drawing_utils

		mid_det_conf = 0.5
		min_track_conf = 0.5

		self.hand_detector = self.mp_hands.Hands(min_detection_confidence=mid_det_conf, min_tracking_confidence=min_track_conf)

		self.run()

	def run(self):
		while True:
			try:
				frame = self.raw_queue.get(0)
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				image = cv2.flip(image, 1)
				image.flags.writeable = False
				results = self.hand_detector.process(image)
				image.flags.writeable = True
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				if results.multi_hand_landmarks:
					for num, hand in enumerate(results.multi_hand_landmarks):
						self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS,
												  self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
												  self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),)
				self.proc_queue.put(image)
			except:
				continue




if __name__=="__main__":
	#https://stackoverflow.com/questions/3671666/sharing-a-complex-object-between-processes
	raw_queue = mproc.Queue()
	proc_queue = mproc.Queue()

	cam = mproc.Process(name='camCap', target=readFrames, args=(raw_queue, proc_queue, ))
	cam.daemon = True

	detector1 = mproc.Process(name='detector1', target=DetectorInstance, args=(raw_queue, proc_queue))
	detector1.daemon = True

	#detector2 = mproc.Process(name='detector2', target=DetectorInstance, args=(raw_queue, proc_queue))
	#detector2.daemon = True
#
	#detector3 = mproc.Process(name='detector3', target=DetectorInstance, args=(raw_queue, proc_queue))
	#detector3.daemon = True
#
	#detector4 = mproc.Process(name='detector4', target=DetectorInstance, args=(raw_queue, proc_queue))
	#detector4.daemon = True

	cam.start()
	detector1.start()
	#detector2.start()
	#detector3.start()
	#detector4.start()

	cam.join()
	detector1.join()
	#detector2.join()
	#detector3.join()
	#detector4.join()








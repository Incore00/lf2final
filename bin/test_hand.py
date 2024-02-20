import cv2
import multiprocessing as mproc
import mediapipe as mp


def readFrames (ns, event):
	# initialize the video capture object
	cap = cv2.VideoCapture(0)
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			ns.frame = frame
			event.set()
			cv2.imshow('Orijinal Frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cap.release()
				cv2.destroyAllWindows()
				return -1
		else:
			return


class MediaPipeRunner(mproc.Process):

	def __init__ (self, name, nsFrame, nsMediaPipe, eventWait, eventPublish):
		super(MediaPipeRunner, self).__init__()

		# Specify a name for the instance
		self.name = name

		# Input and output namespaces
		self.nsFrame = nsFrame
		self.nsMediaPipe = nsMediaPipe

		# Waiter and publisher events
		self.eventWait = eventWait
		self.eventPublish = eventPublish

		# Create a pose estimator from MediaPipe
		mp_pose = mp.solutions.pose

		# Specify pose estimator parameters (static)
		static_image_mode = True
		model_complexity = 1
		enable_segmentation = True  # DONT CHANGE
		min_detection_confidence = 0.5

		# Create a pose estimator here
		self.pose = mp_pose.Pose(
			static_image_mode=static_image_mode,
			model_complexity=model_complexity,
			enable_segmentation=enable_segmentation,
			min_detection_confidence=min_detection_confidence,
			smooth_landmarks=False,
		)

	def run (self):
		while True:
			eventFrame.wait()

			# This part is where it gets stuck:
			results = self.pose.process(cv2.cvtColor(self.nsFrame.frame, cv2.COLOR_BGR2RGB))

			if not results.pose_landmarks:
				continue

			self.nsMediaPipe.segmentation = results.segmentation_mask
			eventMP.set()

if __name__=="__main__":

	mgr = mproc.Manager()

	nsFrame = mgr.Namespace()
	nsMP = mgr.Namespace()

	eventFrame = mproc.Event()
	eventMP = mproc.Event()

	camCap = mproc.Process(name='camCap', target=readFrames, args=(nsFrame, eventFrame, ))
	camCap.daemon=True

	mpCap = MediaPipeRunner('mpCap', nsFrame, nsMP, eventFrame, eventMP, )
	mpCap.daemon=True

	camCap.start()
	mpCap.start()

	camCap.join()
	mpCap.join()
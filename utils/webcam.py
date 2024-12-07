import cv2

class WebcamStream:
    def __init__(self, camera_id="/dev/video0"):
        self.camera_id = camera_id
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_V4L2)

    def read(self):
        if self.cap is None:
            self.start()
        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()
import cv2
import threading


class VideoCaptureThread:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(src)
        self.ret = False
        self.frame = None
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        self.thread.start()
        self.stopped = False
        return self

    def restart(self):
        self.stop()
        self.release()
        self.__init__(self.src)
        self.start()

    def update(self):
        while not self.stopped:
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.src)
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.thread.join()

    def release(self):
        self.cap.release()

    def is_opened(self):
        return self.cap.isOpened()



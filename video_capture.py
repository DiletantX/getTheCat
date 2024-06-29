import datetime

import cv2
import threading
import time
import os


class VideoCaptureThread:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(src)
        self.ret = False
        self.frame = None
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.writer = VideoWriter(self.cap,1)

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
            if not self.writer.finished():
                self.writer.write(self.frame)

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.thread.join()

    def release(self):
        self.cap.release()

    def is_opened(self):
        return self.cap.isOpened()

    def write_short_video(self, duration_seconds):
        print("write_short_video")
        if not self.writer or self.writer.finished():
            print("actually initialize writer")
            self.writer = VideoWriter(self.cap, duration_seconds)


class VideoWriter:
    def __init__(self, cap: cv2.VideoCapture, duration_seconds: int):
        if not cap.isOpened():
            print("Error: Could not initialize video writer.")

        if not os.path.isdir("video"):
            os.mkdir("video")

        # Get the frame width and height
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = 'video/output' + str(current_datetime) + '.mp4'  # Output file name
        self.out = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

        self.num_frames_to_capture = frame_rate * duration_seconds

        self.start_time = time.time()
        self.frame_count = 0
        print("rate = " + str(frame_rate) + ";   w=" + str(frame_width) + "; height=" +
              str(frame_height) + ";   frames to cap = " + str(self.num_frames_to_capture))

    def write(self, frame):
        if self.frame_count < self.num_frames_to_capture:
            # Write the frame to the output file
            #print("writing frame... " + str(self.frame_count))
            self.out.write(frame)
            self.frame_count += 1
            # Display the frame (optional)
            #cv2.imshow('Frame', frame)
            if self.frame_count == self.num_frames_to_capture:
                print("released")
                self.out.release()
        else:
            print("VideoWriter: Unexpected amonut of frames to write to output")
        return

    def finished(self):
        return self.frame_count >= self.num_frames_to_capture




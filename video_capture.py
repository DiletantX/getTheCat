import datetime
import cv2
import threading
import time
import os
import numpy as np
from logger import get_logger

class VideoCaptureThread:
    def __init__(self, src=0, use_knn=False):
        self.mask = None
        self.src = src
        self.cap = cv2.VideoCapture(src)
        self.use_knn = use_knn
        # Initialize background subtractor if KNN mode is enabled
        if self.use_knn:
            self.bg_subtractor = cv2.createBackgroundSubtractorKNN(history=200, dist2Threshold=200, detectShadows=True)
        else:
            self.bg_subtractor = None

        self.ret = False
        self.frame = None
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.writer = VideoWriter(self.cap, 0)
        self.fps = 1

    def start(self):
        self.thread.start()
        self.stopped = False
        return self

    def restart(self):
        self.stop()
        self.release()
        self.__init__(self.src, self.use_knn)
        return self.start()

    def update(self):
        while not self.stopped:
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.src)

            t0 = time.time()
            self.ret, frame = self.cap.read()
            if self.ret:
                self.frame = frame
                if self.use_knn and self.bg_subtractor is not None:
                    # Apply KNN background subtraction to get the foreground mask
                    self.mask = self.bg_subtractor.apply(frame)

                if self.fps == 1:
                    self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

                # Write the frame (or mask) if video writing is active
                if not self.writer.finished():
                    self.writer.write(self.frame)
            else:
                get_logger().debug("No Ret inside video_capture update()")

            if self.fps > 0:
                t_elapsed = time.time() - t0
                time_to_wait = 1 / self.fps - t_elapsed
                if time_to_wait > 0:
                    time.sleep(time_to_wait)


    def read(self):
        return self.ret, self.frame, self.mask, 1

    def read_pre_processed(self):
        if not self.use_knn:
            return self.read()
        elif not self.mask is None and not self.frame is None:
            if len(self.mask.shape) == 3 and self.mask.shape[2] == 3:
                # Convert BGR image to grayscale
                gray = cv2.cvtColor(self.mask, cv2.COLOR_BGR2GRAY)
            else:
                # Frame is already grayscale or in an unexpected format
                gray = self.mask
            avg_intensity = np.mean(gray)
            num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(gray, connectivity=8)
            # Find the label of the largest component (ignore label 0, which is the background)
            if len(stats) > 1:
                largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
            else:
                largest_label = 0
            # Create an empty self.mask and keep only the largest component
            largest_component_mask = np.zeros(gray.shape, dtype=np.uint8)
            largest_component_mask[labels == largest_label] = 255
            threshold_value = avg_intensity * 1.25 + 1
            _, mask_black_white = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
            mask_final = cv2.bitwise_and(mask_black_white,mask_black_white, mask=largest_component_mask)
            masked_frame = cv2.bitwise_and(self.frame, self.frame, mask=mask_final)
            avg_of_final = np.mean(masked_frame)

            return self.ret, masked_frame, mask_final, avg_of_final
        else:
            return None, None, None, 0

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
    def __init__(self, cap: cv2.VideoCapture, duration_seconds):
        if not cap.isOpened():
            print("Error: Could not initialize video writer.")

        if not os.path.isdir("video"):
            os.mkdir("video")

        # Get the frame width, height, and frame rate
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create the VideoWriter object
        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = 'video/output' + str(current_datetime) + '.mp4'

        if duration_seconds > 0:
            self.out = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

        self.num_frames_to_capture = frame_rate * duration_seconds
        self.start_time = time.time()
        self.frame_count = 0
        print("rate = " + str(frame_rate) + "; w=" + str(frame_width) +
              "; height=" + str(frame_height) + "; frames to cap = " + str(self.num_frames_to_capture))

    def write(self, frame):
        if self.frame_count < self.num_frames_to_capture:
            self.out.write(frame)
            self.frame_count += 1
            if self.frame_count == self.num_frames_to_capture:
                print("released")
                self.out.release()
        else:
            print("VideoWriter: Unexpected amount of frames to write to output")
        return

    def finished(self):
        return self.frame_count >= self.num_frames_to_capture

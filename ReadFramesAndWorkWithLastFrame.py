#!/usr/bin/env python

import cv2
import datetime
from imageai.Detection import ObjectDetection
import os
import shutil

from collections import deque




import cProfile
import pstats
import torch
import time

from video_capture import VideoCaptureThread
from telegram_notification import send_telegram_image
import usb_relay

# --- rtsp stream ---
stream_url = 'rtsp://admin:123456@192.168.1.10:554/stream1'
stream2_url = 'rtsp://admin:12345@10.0.0.1:8080/h264.sdp'


def on_press(key):
    try:
        if key.char == 'q':
            print("Q key pressed. Exiting the loop.")
            return False  # Stop listener to exit the loop
    except AttributeError:
        pass


class FrameProcessor:
    def __init__(self):
        self.execution_path = os.getcwd()
        self.detector = ObjectDetection()
        #self.detector.useCPU()
        print("CUDA is available: " + str(torch.cuda.is_available()))
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(os.path.join(self.execution_path, "..//yolov3.pt"))
        # detector.setModelTypeAsTinyYOLOv3() # tiny YOLOv3 is faster, but detacts only one person on the test image
        #self.detector.setModelTypeAsRetinaNet()
        #self.detector.setModelPath(os.path.join(self.execution_path, "..//retinanet_resnet50_fpn_coco-eeacb38b.pth"))
        self.detector.loadModel()
        self.custom_objects = self.detector.CustomObjects(cat=True, person=True, dog=True)
        if not os.path.isdir("detections"):
            os.mkdir("detections")
        self.persons_index_queue = deque(maxlen=3)

    def process_single_frame(self, frame):
        print("-....", end='')
        detections = self.detector.detectObjectsFromImage(input_image=frame,
                                                          output_image_path=os.path.join(self.execution_path, "last.jpg"),
                                                          minimum_percentage_probability=20,
                                                          custom_objects=self.custom_objects)
        print("...+")
        detected = False
        person = False
        for eachObject in detections:
            print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
            print("--------------------------------")
            current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            new_file_name = "detections/" + eachObject["name"] + current_datetime + ".jpg"
            shutil.copyfile("last.jpg", new_file_name)
            if eachObject["name"] == "person":
                person = True

            else:
                detected = True

        if sum(self.persons_index_queue) >= 2:
            if detected or person:
                send_telegram_image(new_file_name, "Paused due to many persons" + str(current_datetime))
            print("persons were detected recently")
            time.sleep(30)
            detected = False
        else:
            if detected:
                send_telegram_image(new_file_name, "Animals detected!" + str(current_datetime))

        self.persons_index_queue.append(int(person))

        return detected


def main():
    # open stream
    #profiler = cProfile.Profile()
    #profiler.enable()
    fp = FrameProcessor()
    #fp2 = FrameProcessor()
    t_start = datetime.datetime.now()

    #cap = VideoCaptureThread(stream_url).start()
    #cap2 = VideoCaptureThread(stream2_url).start()
    # For test: from default camera which normally has ID = 0 (if camera exists on device)

    cap = VideoCaptureThread().start()

    print("Press 'Q' to quit the loop.")

    while True:
        ret, frame = cap.read()
        print("*...", end='')
        if ret:
            detected = fp.process_single_frame(frame)
            if detected:
                cap.write_short_video(10)
                usb_relay.relay_on_for_x_sec(10)
        print("...*")

        if not ret:
            print("not ret")
            time.sleep(5)
            ret, frame = cap.read()
            if not ret:
                print("had to restart video capturing")
                cap = cap.restart()


        time.sleep(2)


    delta_t = datetime.datetime.now() - t_start
    print("Process took " + str(delta_t))

    cap.stop()
    cap.release()
    cv2.destroyAllWindows()
    #profiler
    #profiler.disable()
    #stats = pstats.Stats(profiler)
    #stats.sort_stats('cumtime').print_stats(15)


if __name__ == '__main__':
    main()

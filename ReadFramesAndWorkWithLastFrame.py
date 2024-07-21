#!/usr/bin/env python

import cv2
import datetime
from imageai.Detection import ObjectDetection
import os
import shutil

from playsound import playsound
import cProfile
import pstats
import torch
import time

from video_capture import VideoCaptureThread
from telegram_notification import send_telegram_image
import usb_relay

# --- rtsp stream ---
stream_url = 'rtsp://admin:123456@192.168.1.10:554/stream1'


def alarm_sound():
    audio_file = os.path.dirname(__file__) + '\\mixkit-angry-cartoon-kitty-meow-94.wav'
    try:
        playsound(audio_file, True)
    except:
        print("Error with sound notification!!!")


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

    def process_single_frame(self, frame):
        print("-....", end='')
        detections = self.detector.detectObjectsFromImage(input_image=frame,
                                                          output_image_path=os.path.join(self.execution_path, "last.jpg"),
                                                          minimum_percentage_probability=20,
                                                          custom_objects=self.custom_objects)
        print("...+")
        detected = False
        for eachObject in detections:
            print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
            print("--------------------------------")
            current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            new_file_name = "detections/" + eachObject["name"] + current_datetime + ".jpg"
            shutil.copyfile("last.jpg", new_file_name)
            if eachObject["name"] == "cat":
                alarm_sound()
                send_telegram_image(new_file_name, "Cat detected"+str(current_datetime))
                detected = True
            elif eachObject["name"] != "person":
                detected = True
                send_telegram_image(new_file_name, "Some animals detected"+str(current_datetime))

        return detected


def main():
    # open stream
    #profiler = cProfile.Profile()
    #profiler.enable()
    fp = FrameProcessor()
    t_start = datetime.datetime.now()

    cap = VideoCaptureThread(stream_url).start()
    # For test: from default camera which normally has ID = 0 (if camera exists on device)
    #cap = VideoCaptureThread().start()

    while True:
    #for i in range(1,21):
        ret, frame = cap.read()
        print("*...", end='')
        if ret:
            detected = fp.process_single_frame(frame)
            if detected:
                cap.write_short_video(10)
                usb_relay.relay_on_for_x_sec(10)

        #print("..." + str(i) + " detections done")
        print("...*")
        time.sleep(2)

        if not ret:
            print("not ret")
            time.sleep(5)
            ret, frame = cap.read()
            if not ret:
                print("had to restart video capturing")
                cap = cap.restart()


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

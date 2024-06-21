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
        self.custom_objects = self.detector.CustomObjects(cat=True, person=True, dog=True, bird=True, cow=True, horse=True)

    def process_single_frame(self, frame):

        detections = self.detector.detectObjectsFromImage(input_image=frame,
                                                          output_image_path=os.path.join(self.execution_path, "last.jpg"),
                                                          minimum_percentage_probability=30,
                                                          custom_objects=self.custom_objects)
        for eachObject in detections:
            if eachObject["name"] == "cat":
                alarm_sound()
            print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
            print("--------------------------------")
            current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            new_file_name = "detections/" + eachObject["name"] + current_datetime + ".jpg"
            if not os.path.isdir("detections"):
                os.mkdir("detections")
            shutil.copyfile("last.jpg", new_file_name)
            if eachObject["name"] == "cat":
                send_telegram_image(new_file_name, "Cat detected"+str(current_datetime))
            #elif eachObject["name"] != "person":
            #    send_telegram_image(new_file_name, "Some animals detected")



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

        if ret:
            fp.process_single_frame(frame)

        #print("..." + str(i) + " detections done")

        time.sleep(0.8)

    delta_t = datetime.datetime.now() - t_start
    print("Process took " + str(delta_t))

    cap.stop()
    cap.release()
    cv2.destroyAllWindows()
    #profiler
    #profiler.disable()
    #stats = pstats.Stats(profiler)
    #stats.sort_stats('cumtime').print_stats(15)


main()

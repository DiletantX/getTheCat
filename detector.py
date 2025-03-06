import datetime
import os
import shutil
import time
from collections import deque

import torch
from imageai.Detection import ObjectDetection
from logger import get_logger

from telegram_notification import send_telegram_image

LAST_JPG = "last.jpg"


class FrameProcessor:
    def __init__(self):
        get_logger().info("FrameProcessor Initializing Started")
        self.execution_path = os.getcwd()
        self.detector = ObjectDetection()
        self.detector.useCPU()
        get_logger().info("CUDA is available: " + str(torch.cuda.is_available()))
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(os.path.join(self.execution_path, "..//yolov3.pt"))
        # detector.setModelTypeAsTinyYOLOv3() # tiny YOLOv3 is faster, but detacts only one person on the test image
        #self.detector.setModelTypeAsRetinaNet()
        #self.detector.setModelPath(os.path.join(self.execution_path, "..//retinanet_resnet50_fpn_coco-eeacb38b.pth"))
        self.detector.loadModel()
        self.custom_objects = self.detector.CustomObjects(cat=True, person=True, dog=True)
        if not os.path.isdir("detections"):
            os.mkdir("detections")
        self.persons_index_queue = deque(maxlen=10)
        get_logger().info("FrameProcessor Initializing Complete")

    def process_single_frame(self, frame):
        get_logger().debug("-....")
        detections = self.detector.detectObjectsFromImage(input_image=frame,
                                                          output_image_path=os.path.join(self.execution_path, LAST_JPG),
                                                          minimum_percentage_probability=20,
                                                          custom_objects=self.custom_objects)
        get_logger().debug("...+")
        detected = False
        person = False

        if detections:
            current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            for detected_object in detections:
                get_logger().info(str(detected_object["name"]) + " : " + str(detected_object["percentage_probability"]) + " : " + str(detected_object["box_points"]))
                get_logger().info("--------------------------------")
                new_file_name = "detections/" + detected_object["name"] + current_datetime + ".jpg"
                shutil.copyfile(LAST_JPG, new_file_name)
                if detected_object["name"] == "person" and detected_object["percentage_probability"] > 90:
                    person = True
                elif detected_object["name"] != "person":
                    detected = True

            if sum(self.persons_index_queue) >= 3:
                if detected or person:
                    send_telegram_image(LAST_JPG, "Paused due to many persons" + str(current_datetime))
                get_logger().info("persons were detected recently")
                time.sleep(30)
                detected = False
            else:
                if detected:
                    send_telegram_image(LAST_JPG, "Animals detected!" + str(current_datetime))

        self.persons_index_queue.append(int(person))

        return detected

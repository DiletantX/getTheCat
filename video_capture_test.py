import unittest
from time import sleep
import time

from video_capture import VideoCaptureThread
import cv2 as cv
import numpy as np

class MyTestCase(unittest.TestCase):
    def test_video_capture(self):

        #print("OpenCV version:", cv.__version__)
        #print("FFmpeg support:", cv.getBuildInformation())
        fps = 7
        frame_duration = 1.0 / fps
        cap = VideoCaptureThread("test_videos/output.mp4", use_knn=True).start()

        while cap.is_opened():
            t0 = time.time()
            ret, frame, mask, score = cap.read_pre_processed()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                sleep(1)
            else:

                cv.imshow('frame', frame )






            t_elapsed = time.time() - t0
            t_to_wait = frame_duration - t_elapsed
            if t_to_wait > 0:
                time.sleep(t_to_wait)

            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()

        self.assertEqual(True, False)  # add assertion here

    def test_cv_sample_code(self):

        cap = cv.VideoCapture("http://193.214.77.234:8001/axis-cgi/mjpg/video.cgi")
        fourcc = cv.VideoWriter.fourcc(*'X264')
        out = False
        counter = 0
        t0 = time.time()

        while cap.isOpened():
            counter = counter + 1

            if not out:
                frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
                frame_rate = int(cap.get(cv.CAP_PROP_FPS))

                print("Frame rate = " + str(frame_rate))

                out = cv.VideoWriter('out.mp4', fourcc, 3, (frame_width, frame_height))

            ret, frame = cap.read()

            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            out.write(frame)

            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        t_end = time.time() - t0
        print("Elapsed Time = " + str(t_end))
        print("Processed frames = " + str(counter))
        cap.release()
        out.release()
        cv.destroyAllWindows()


        self.assertEqual(True, False)  # add assertion here




if __name__ == '__main__':
    unittest.main()

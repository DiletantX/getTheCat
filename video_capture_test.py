import unittest
from time import sleep
import time

from video_capture import VideoCaptureThread
import cv2 as cv

class MyTestCase(unittest.TestCase):
    def test_video_capture(self):

        print("OpenCV version:", cv.__version__)
        print("FFmpeg support:", cv.getBuildInformation())

        cap = VideoCaptureThread("http://193.214.77.234:8001/axis-cgi/mjpg/video.cgi").start()
        video = False
        sleep(5)

        while cap.is_opened():

            if not video:
                video = True
                cap.write_short_video(10)

            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            cv.imshow('frame', frame)
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

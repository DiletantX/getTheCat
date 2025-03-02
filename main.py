#!/usr/bin/env python

import cv2
import datetime
import time
from logger import get_logger

from detector import FrameProcessor
from video_capture import VideoCaptureThread
import usb_relay

# --- rtsp stream ---
stream_url = 'rtsp://admin:123456@192.168.1.10:554/stream1'
stream2_url = 'rtsp://admin:12345@10.0.0.1:8080/h264.sdp'


def main():
    get_logger().info("getTheCat main script started")
    #profiler = cProfile.Profile()
    #profiler.enable()
    fp = FrameProcessor()
    #fp2 = FrameProcessor()
    t_start = datetime.datetime.now()
    cap = VideoCaptureThread(stream_url).start()
    #cap2 = VideoCaptureThread(stream2_url).start()
    # For test: from default camera which normally has ID = 0 (if camera exists on device)

    #cap = VideoCaptureThread().start()

    print("Press 'Q' to quit the loop.")

    while True:
        ret, frame = cap.read()
        get_logger().debug("*...")
        if ret:
            detected = fp.process_single_frame(frame)
            if detected:
                cap.write_short_video(10)
                usb_relay.relay_on_for_x_sec(10)
        get_logger().debug("...*")

        if not ret:
            get_logger().error("Video capturing didn't return any output. May be, the camera is unreachable or overloaded. Will try to wait a few seconds and restart capturing ")
            time.sleep(5)
            ret, frame = cap.read()
            if not ret:
                get_logger().info("Attempting to restart video capturing...")
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

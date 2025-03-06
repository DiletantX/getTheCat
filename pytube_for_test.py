import numpy as np
import cv2
import mss
import time

# Define the screen area to capture (adjust top, left, width, and height as needed)
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1100}
fps = 7
frame_duration = 1.0 / fps
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter.fourcc(*'mp4v')
output_file = "test_videos/output.mp4"
out = cv2.VideoWriter(output_file, fourcc, fps, (monitor["width"], monitor["height"]))
time.sleep(5)
t_end = time.time() + 100

with mss.mss() as sct:
    while time.time() < t_end :
        t0 = time.time()
        # Capture the screen
        img = np.array(sct.grab(monitor))
        # Convert BGRA to BGR format for OpenCV
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Write the frame to the video file
        out.write(frame)
        elapsed_t = time.time() - t0
        delta =  frame_duration - elapsed_t
        if delta > 0:
            time.sleep(delta)


        # Optional: display the captured frame in a window
        #cv2.imshow("Screen Capture", frame)
        #if cv2.waitKey(1) & 0xFF == ord("q"):
        #    break

# Release the video writer and close windows
out.release()
cv2.destroyAllWindows()

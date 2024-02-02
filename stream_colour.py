import cv2
from utils import choose_colour, get_limits, base_colour_selection, stay_center, color_and_contour_detection, land_if_distance_sufficient, videoRecorder, simple_colour_detection
from djitellopy import Tello
import numpy as np
import time
from threading import Thread
#from params import HEIGHT_FRAME, WIDTH_FRAME

#simple test colour
colour_name = "green"
lower_limit = np.array([45,109,0],dtype=np.uint8)
upper_limit = np.array([76,206,255],dtype=np.uint8)

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}%")

tello.streamon()

recorder = Thread(target=videoRecorder, args=(tello,))
recorder.start()

while True:
    frame = tello.get_frame_read().frame.copy()

    frame_w_r = simple_colour_detection(frame, colour_name, lower_limit, upper_limit)

    # Display the edited frame
    cv2.imshow('Tello Video Stream', frame_w_r)
    time.sleep(1/25)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cv2.destroyAllWindows()

# Stop the recording thread
keepRecording = False
recorder.join()

# Disconnect and land the Tello drone
tello.streamoff()
tello.land()

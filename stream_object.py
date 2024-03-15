import cv2
from utils import choose_colour, get_limits, base_colour_selection, stay_center, color_and_contour_detection, land_if_distance_sufficient
from djitellopy import Tello
import numpy as np

#simple test colour
colour_name, lowerLimit, upperLimit = base_colour_selection()


# multiple test colours
searching_colour, colour_name = choose_colour()
print(colour_name)
print(searching_colour)

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}%")
tello.streamon()

##tello.takeoff()

# Params of rotation:
max_rotation_attempts = 4
rotation_attempts = 0

# Define the UDP video stream URL
video_stream_url = "udp://0.0.0.0:11111"
feed = cv2.VideoCapture(video_stream_url)

while True:
    ret, frame = feed.read()
    # Shape Check Tello: 480, 640 , 3

    result_frame, cx , cy, M  = color_and_contour_detection(frame=frame,lower_limit=lowerLimit,upper_limit=upperLimit)

    # loop for no object found
    if cx == 0:
        print("No coloured Object found. Roate...")
        tello.rotate_clockwise(90)
        rotation_attempts += 1

    else:
        stay_center(cx, cy, frame.shape[1])
        print(f"Found a {colour_name} in the {rotation_attempts}th attempt")

        cv2.imwrite(f'photo_{rotation_attempts}.jpg', result_frame)
        print(f'Photo {rotation_attempts} taken.')


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Video-Feed freigeben und Fenster schließen
##land_if_distance_sufficient(tello=tello,min_distance=1.70)
keepRecording = False
feed.release()
cv2.destroyAllWindows()

# Disconnect und Land the Tello drone
tello.streamoff()

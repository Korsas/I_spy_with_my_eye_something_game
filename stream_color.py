import cv2
from utils import choose_colour, get_limits, base_colour_selection
from PIL import Image
from djitellopy import Tello
import numpy as np

#simple test colour
##colour_name, lowerLimit, upperLimit = base_colour_selection()


# multiple test colours
searching_colour, colour_name = choose_colour()
print(colour_name)
print(searching_colour)

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}%")
tello.streamon()

# Define the UDP video stream URL
video_stream_url = "udp://0.0.0.0:11111"
feed = cv2.VideoCapture(video_stream_url)



#feed = cv2.VideoCapture(0)

while True:
    ret, frame = feed.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=searching_colour)



    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    #contours and noice cancellation
    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)



    #colour_mask = cv2.bitwise_and(frame,frame,mask=mask)

    # stack all views
    mask_fit= cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    interface = np.hstack((frame, mask_fit))

    cv2.imshow(f'Color Track: {colour_name}', interface)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video capture object and close the display window
feed.release()
cv2.destroyAllWindows()

# Disconnect and land the Tello drone
tello.streamoff()
tello.land()

import cv2
from utils import choose_colour, get_limits
from PIL import Image
from djitellopy import Tello

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}%")
tello.streamon()

# Define the UDP video stream URL
video_stream_url = "udp://0.0.0.0:11111"
feed = cv2.VideoCapture(video_stream_url)

yellow = [0, 255, 255]

searching_colour = choose_colour()

#feed = cv2.VideoCapture(0)

while True:
    ret, frame = feed.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    #contours and noice cancellation
    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

    cv2.imshow('Color Track', mask)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video capture object and close the display window
feed.release()
cv2.destroyAllWindows()

# Disconnect and land the Tello drone
tello.streamoff()
tello.land()

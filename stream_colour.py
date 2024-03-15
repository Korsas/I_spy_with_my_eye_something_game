import cv2
from utils import choose_colour,simple_colour_detection, stay_center,land_if_distance_sufficient, video_recorder
from djitellopy import Tello
import numpy as np
import time
from threading import Thread
import logging

# Configure logging to output debug messages to console
logging.basicConfig(level=logging.DEBUG)

#simple test colour
colour_name = "green"
lower_limit = np.array([45,109,0],dtype=np.uint8)
upper_limit = np.array([76,206,255],dtype=np.uint8)


#random test colour
#colour_name, lower_limit, upper_limit = base_colour_selection()
print(colour_name)

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}%")
tello.streamon()

for i in range(3):
    print(f"Drone takeoff in {3-i}")
tello.takeoff()

# Params of rotation:
max_rotation_attempts = 4
rotation_attempts = 0
images_taken = 0
max_images_per_rotation = 5
scale = 3

# Define the UDP video stream URL. More Info here: https://docs.opencv.org/4.5.2/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
video_stream_url = "udp://0.0.0.0:11111"
feed = cv2.VideoCapture(video_stream_url)

fps = feed.get(5)
#fps = cv2.CAP_PROP_FPS
width = feed.get(3) #alternative: cv2.CAP_PROP_FRAME_WIDTH
height = feed.get(4) # alternative: cv2.CAP_PROP_FRAME_HEIGHT
frames = cv2.CAP_PROP_FRAME_COUNT
print(f"Frames per second : '{fps}'FPS, width = '{width}' , height = '{height}")

captured = False
##ret, result_frame = feed.read()
time.sleep(1)

##video = Thread(target=video_recorder(frame=result_frame))
##video.start()
no_coords_time = None

while rotation_attempts < max_rotation_attempts:
    ret, frame = feed.read()
    # Shape Check Tello: 480, 640 , 3
    height , width , layers =  frame.shape
    new_h=int(height/scale)
    new_w=int(width/scale)
    resize = cv2.resize(frame, (new_w, new_h)) # <- resize for improved performance

    result_frame,x_mid,y_mid,coords = simple_colour_detection(frame=frame,colour_name=colour_name,lower_limit=lower_limit,upper_limit=upper_limit)

      # Überprüfen, ob Koordinaten erkannt wurden
    if coords is None:
        # Wenn keine Koordinaten erkannt wurden, starte die Zeitmessung
        if no_coords_time is None:
            no_coords_time = time.time()
        else:
            # Überprüfe, ob die Zeitdauer von 5 Sekunden abgelaufen ist
            if time.time() - no_coords_time >= 5:
                print("No coloured Object found for 5 seconds. Rotate...")
                tello.rotate_clockwise(90)
                ##tello.send_control_command("cw 90")
                rotation_attempts += 1
                # Zurücksetzen der Zeitmessung, wenn die Drohne gedreht wurde
                no_coords_time = None
    else:
        # Koordinaten wurden erkannt, zurücksetzen der Zeitmessung
        no_coords_time = None
        ##stay_center(x_mid, y_mid, frame.shape[1])
        if not captured:
            if images_taken < max_images_per_rotation:
                cv2.imwrite(f'photo_{colour_name}_{rotation_attempts}_{images_taken}.jpg', result_frame)
                print(f'Photo {rotation_attempts} taken.')
                captured = True
                images_taken += 1
            else:
                print("Maximum number of images per rotation reached.")



        ##video.write(result_frame)
        ##time.sleep(1 / 25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video-Feed freigeben und Fenster schließen
land_if_distance_sufficient(tello=tello,min_distance=1.70)
feed.release()
cv2.destroyAllWindows()

# Disconnect und Land the Tello drone
tello.streamoff()

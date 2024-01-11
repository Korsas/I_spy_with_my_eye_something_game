from djitellopy import Tello
from ultralytics import YOLO
import cv2

drone = Tello()
drone.connect()
print(drone.get_battery)

drone.takeoff()
print(drone.get_current_state)
print(drone.get_height)

drone.land()

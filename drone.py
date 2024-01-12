from djitellopy import Tello
from ultralytics import YOLO
import cv2

drone = Tello()
drone.connect()
battery = drone.get_battery()
print(f"battery status: {battery}%")
Stream()
drone.takeoff()
state = drone.get_current_state()
print(state)
drone.rotate_clockwise(90)
height_position = drone.get_height()
print(f"{height_position} cm")
drone.land()

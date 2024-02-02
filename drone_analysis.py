from djitellopy import Tello
from utils import land_if_distance_sufficient
import time

# Connect Tello + Status
drone = Tello()
drone.connect()
battery = drone.get_battery()
print(f"battery status: {battery}%")
drone.takeoff()


imu_data = drone.query_attitude()
print("IMU Data:", imu_data)
time.sleep()

# Tello height basic meassurement
# tof = 81 cm distance_ground = 70 cm

height_position = drone.get_height()
tof = drone.get_distance_tof()
print(f"{height_position} cm")
print(f"TOF = {tof}")


drone.move_up(x=100)
drone.rotate_counter_clockwise(90)

imu_data = drone.query_attitude()
print("IMU Data:", imu_data)

time.sleep(3)



land_if_distance_sufficient(tello=drone,min_distance=1.73)

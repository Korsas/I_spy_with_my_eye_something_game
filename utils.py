import cv2
import random
import numpy as np
import time
from djitellopy import Tello

colours_lib_basis = ["red","green","blue"]
colours_lib = ["yellow","red","green","blue","orange","pink","brown","grey"]
colour_selection = {"yellow":[0,255,255],"red":[0,0,255],"green":[0,153,0],"blue":[255,0,0],"orange":[0,128,255],"pink":[203,192,255],"brown":[19,69,139],"grey":[128,128,128]}


def choose_colour(list_names=colours_lib,colour_codes=colour_selection):
    # Colours in BGR colorspaces
    selected_colour = random.choice(list_names)
    colour = colour_codes.get(selected_colour)
    print(f"Wähle {selected_colour} mit Code {colour}")
    return colour, selected_colour

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

def base_colour_selection(list_names_hardcoded=colours_lib_basis):
    # hardcoded optimized colours
    selected_colour = random.choice(list_names_hardcoded)
    if selected_colour == "red":
        lowerLimit = np.array([161,155,84])
        upperLimit = np.array([179,255,255])
    elif selected_colour == "blue":
        lowerLimit = np.array([94,80,2])
        upperLimit = np.array([126,255,255])
    elif selected_colour == "green":
        lowerLimit = np.array([25,52,72])
        upperLimit = np.array([102,255,255])

    return selected_colour,lowerLimit,upperLimit


def land_if_distance_sufficient(tello,min_distance=1.65):
    tello = Tello()
    # Warte auf stabile Messungen vom TOF-Sensor
    time.sleep(5)

    # Lese die TOF-Entfernung
    while True:
        current_height = tello.get_distance_tof()

        #print(f"TOF Distance: {tof_distance} m")

        # Überprüfe, ob die gemessene Entfernung ausreichend ist
        if current_height is not None and current_height >= min_distance:
            print("Sichere Landung möglich. Starte Landeprozess.")
            tello.land()
            break
        else:
            print("Nicht genügend Platz zum Landen oder unzureichende TOF-Daten.")
            tello.move_forward(10)
            time.sleep(0.1)

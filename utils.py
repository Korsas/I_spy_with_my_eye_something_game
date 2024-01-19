import cv2
import random
import numpy as np

colours_lib = ["yellow","red","green"]
colour_selection = {"yellow":[0,255,255],"red":[0,0,255],"green":[0,255,0]}

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

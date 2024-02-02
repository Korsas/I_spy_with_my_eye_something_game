import cv2
import random
import numpy as np
import time
from djitellopy import Tello
#from params import HEIGHT_FRAME, WIDTH_FRAME


# base_colour lib
colours_lib_basis = ["red","blue","orange","purple","pink","yellow"]


# choose_colour öob
colours_lib = ["yellow","red","green","blue"]
colour_selection = {"yellow":[0,255,255],"red":[0,0,255],"green":[0,153,0],"blue":[255,0,0],"brown":[19,69,139],"black":[0,0,0],"white":[255,255,255]}
colour_objects = []

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
    print(f"{selected_colour}")

    if selected_colour == "red":
        # Set Up on Tello red
        lowerLimit = np.array([0,168,0],dtype=np.uint8)
        upperLimit = np.array([6,255,239],dtype=np.uint8)
    if selected_colour == "blue":
        # Set Up on Tello blue
        lowerLimit = np.array([78,35,2],dtype=np.uint8)
        upperLimit = np.array([134,255,160],dtype=np.uint8)
    if selected_colour == "green":
        # Set Up on Tello dark green
        lowerLimit = np.array([45,109,0],dtype=np.uint8)
        upperLimit = np.array([76,206,255],dtype=np.uint8)
    if selected_colour == "orange":
        # Set Up on Tello dark orange
        lowerLimit = np.array([7.5,168,0],dtype=np.uint8)
        upperLimit = np.array([18,255,255],dtype=np.uint8)
    if selected_colour == "white":
        lowerLimit = np.array([0,0,165],dtype=np.uint8)
        upperLimit = np.array([179,255,255],dtype=np.uint8)
    if selected_colour == "black":
        lowerLimit = np.array([0,0,0],dtype=np.uint8)
        upperLimit = np.array([131,255,56],dtype=np.uint8)
    if selected_colour == "pink":
        # Set Up on Tello light pink
        lowerLimit = np.array([125,71,163],dtype=np.uint8)
        upperLimit = np.array([177,255,255],dtype=np.uint8)
    if selected_colour == "purple":
        lowerLimit = np.array([121,63,94],dtype=np.uint8)
        upperLimit = np.array([161,219,145],dtype=np.uint8)
    if selected_colour == "yellow":
        # Set Up on Tello yellow
        lowerLimit = np.array([18,160,45],dtype=np.uint8)
        upperLimit = np.array([26,255,255],dtype=np.uint8)
    else: print(f"return value {selected_colour} not available!")

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

def stay_center(cx,cy,frame_width):
    if cx is not None and cy is not None:
        distance_to_center = cx - frame_width/2
        print(f"Distance to center: {distance_to_center}")

        if distance_to_center > 100:
            print(f"Balance right direction: {distance_to_center}")
            Tello.move_right(distance_to_center)
        elif distance_to_center < -100:
            print(f"Balance left direction: {distance_to_center}")
            Tello.move_left(abs(distance_to_center))

        else:
            print("Stay centered")

    else:
        print("No valid contours found. Adjust your logic accordingly.")

def color_and_contour_detection(frame, lower_limit, upper_limit):
    interface = frame.copy()
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
    combine_colour = cv2.bitwise_and(frame,frame,mask=color_mask)
    color_mask = cv2.cvtColor(color_mask,cv2.COLOR_GRAY2BGR)
    blur_img = cv2.GaussianBlur(color_mask,(7,7),1)
    gray_img_blur = cv2.cvtColor(blur_img,cv2.COLOR_BGR2GRAY)


    edges = cv2.Canny(gray_img_blur,150,100)

    kernel_dil = np.ones((5,5))

    imgDil = cv2.dilate(edges,kernel=kernel_dil,iterations=1)

    cx, cy, M = None, None, None
    # Konturen finden und filtern
    contours, _ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Flächencheck
    valid_contours = [cnt for cnt in contours if 300 < cv2.contourArea(cnt) < 6000]
    ##valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)

    if valid_contours:
        # select out of the three biggest
        random_conture = random.choice(valid_contours)
        masked_contour = cv2.bitwise_and(random_conture, random_conture, mask=color_mask)

        if np.any(masked_contour):
            epsilon = 0.02*cv2.arcLength(random_conture, closed=True)
            approx = cv2.approxPolyDP(random_conture,epsilon=epsilon,closed=True)
            M = cv2.moments(random_conture)
            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

            # Zeichnen Sie die Kontur und den Mittelpunkt
            coords = (cx,cy)
            cv2.drawContours(frame, [random_conture], 0, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame,random_conture,coords,fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1,color=(0,0,0),thickness=1)

    return frame, cx, cy, M

def simple_colour_detection(frame,colour_name, lower_limit, upper_limit):
    while True:
        interface = frame.copy()
        # Shape Check Tello: 480, 640 , 3

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImage, lower_limit, upper_limit)
        result = cv2.bitwise_and(frame,frame,mask=mask)

        # so it can be displayable (otherwise wrong dimension)
        mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)

        #contours and noice cancellation
        imgBlur = cv2.GaussianBlur(result,(7,7),1)

        # so it can be displayable (otherwise wrong dimension). Alo Gray for Contours
        imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(imgGray,100,150)

        kernel_dil = np.ones((5,5))

        imgDil = cv2.dilate(edges,kernel=kernel_dil,iterations=1)

        contours, hierachy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            for contour in contours:
                #filter out under 800 pixels and above 10k pixels
                if cv2.contourArea(contour) > 400:
                    #Refine Contours
                    cv2.drawContours(interface,contour,0,(0,0,0),4)
                    epsilon = 0.02*cv2.arcLength(contour, closed=True)
                    approx = cv2.approxPolyDP(contour,epsilon=epsilon,closed=True)

                    #Take parameters and mark the object
                    x, y, w, h = cv2.boundingRect(approx)
                    x_mid = int(x + w/3)
                    y_mid = int(y + h/1.5)
                    coords = (x_mid,y_mid)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(frame,colour_name,coords,fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1,color=(0,0,0),thickness=1)
        return frame



def videoRecorder(tello,fps=25,fourcc='XVID'):
    global keepRecording
    global colour_name
    global lower_limit
    global upper_limit
    keepRecording = True
    # only with get_frame_read()
    frame = tello.get_frame_read().frame
    height, width, _ = frame.shape

    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*str(fourcc)), fps, (width, height))

    while keepRecording:
        frame = tello.get_frame_read().frame
        frame_w_r = simple_colour_detection(frame, colour_name, lower_limit, upper_limit)

        frame_w_r= cv2.cvtColor(frame_w_r, cv2.COLOR_GRAY2RGB)
        video.write(frame_w_r)
        time.sleep(1/30)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()

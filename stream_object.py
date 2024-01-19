import cv2
from djitellopy import Tello
from ultralytics import YOLO

# Initializing the Tello drone
tello = Tello()
tello.connect()
print(f"Battery Status: {tello.get_battery()}")
tello.streamon()

# Define the UDP video stream URL

fifo_size = "?fifo_size=278876"
# 50*1024*1024/188 = 278876,595744681
non_fatal_set = "&overrun_nonfatal=1"
secondary_ip = "udp://192.168.10.1:11111"
cam_ip = "udp://0.0.0.0:11111"

video_stream_url = f"{secondary_ip}{fifo_size}{non_fatal_set}"
print(video_stream_url)
feed = cv2.VideoCapture(video_stream_url)

#feed = cv2.VideoCapture(0)

model = YOLO("yolov8n.pt")
frame_counter = 0

while True:
    # Read a frame from the video
    ret, frame = feed.read()
    frame_counter += 1
    print(frame_counter)

    # Run YOLOv8 inference on the frame
    results = model(source=frame, stream=True)
    written_results = model.predict(source=frame,stream=True)


    # Visualize the results on the frame
    annotated_frame = next(results).plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release the video capture object and close the display window
feed.release()
cv2.destroyAllWindows()

# Disconnect and land the Tello drone
tello.streamoff()
tello.land()

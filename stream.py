import cv2
import os

tello_port = os.environ.get("Port")
tello_ip = os.environ.get("IP")
tello_video = cv2.VideoCapture(f'udp://{tello_ip}:{tello_port}')

while True:
    try:
        ret,frame = tello_video.read()
        if ret == True:
            cv2.imshow(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as err:
        print(err)

tello_video.release()
cv2.destroyAllWindows()

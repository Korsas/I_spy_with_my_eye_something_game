
import cv2
import time
from djitellopy import Tello
import argparse
#from params import WIDTH_FRAME, HEIGHT_FRAME
from ultralytics import YOLO
import supervision as sv
import numpy as np

ZONE_POLYGON = np.array([
    [0, 0],
    [1280 // 2, 0],
    [1280 // 2, 720],
    [0, 720]
])



def parse_feed() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Yolov8 Feed")
    parser.add_argument(
        "--webcam-resolution",
        default=[1280,720],
        nargs=2,
        type=int
    )

    args = parser.parse_args()
    return args

def main():
    # Yolov8 Transfer Feed
    args = parse_feed()
    frame_width,frame_height = args.webcam_resolution
    tello = Tello()
    tello.connect()

    tello.streamoff()
    tello.streamon()

    vidfeed = cv2.VideoCapture("udp://0.0.0.0:11111?fifo_size=50000000&overrun_nonfatal=1")
    vidfeed.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    vidfeed.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)

    model = YOLO("yolov8n-cls.pt",task="detect")

    box_annotator = sv.BoxAnnotator(thickness=2,text_thickness=2,text_scale=1)


    zone = sv.PolygonZone(polygon=ZONE_POLYGON, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )
    time.sleep(500)

    while True:

        ret,frame = vidfeed.read()
        yolo_result = model(frame)[0]

        if frame is not None:
            cv2.imshow("Video Streaming", frame)

        #Test Start
        if yolo_result is not None and yolo_result.boxes is not None:
        #Test END
            detections = sv.Detections.from_yolov8(yolo_result)

            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, _
                in detections
            ]

            frame = box_annotator.annotate(
                scene=frame,
                detections=detections,
                labels=labels
            )

            zone.trigger(detections=detections)
            frame = zone_annotator.annotate(scene=frame)
            # Tello App way of doing it:
            # use this for frame by Tello only: frame_read = tello.get_frame_read()
            # use this for frame by Tello only: myFrame = frame_read.frame
            # Strandard Resolution = 720x960x3: print(frame.shape)



        if cv2.waitKey(30) == 27:
            frame.stop()
            tello.streamoff()
            break

if __name__ == "__main__":
    main()

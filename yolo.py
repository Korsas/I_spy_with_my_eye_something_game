import os
import cv2
from ultralytics import YOLO

# Lade das YOLOv8-Modell
model = YOLO('yolov8n.pt')

# Pfadeinstellungen
input_folder = '.'  # Der aktuelle Ordner, in dem sich auch die Bilder befinden
rate_bilder = 'output_images'  # Pfad zum Ordner für die Ausgabebilder
os.makedirs(rate_bilder, exist_ok=True)  # Erstelle den Ausgabebilderordner, falls er nicht existiert

# Iteriere durch alle Bilddateien im Eingangsordner
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # only pics
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Führe YOLOv8-Inferenz auf dem Bild durch
        model.predict(image, save=True)


        print(f'Riddle item {filename} created.')

print('Done.')

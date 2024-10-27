import cv2
import torch
from ultralytics import YOLOv10 as YOLO
import json
import base64

def useModelFromBase64 (string64):
    with open("imageToPredict.png", "wb") as fh:
        fh.write(base64.b64decode(string64))
    model = YOLO('best.pt')  # or another version of YOLOv8 (e.g., yolov8s.pt for small)
    input_image = 'imageToPredict.png'
    image = cv2.imread(input_image)
    results = model(image)[0]
    results.save("static/results_image0.jpg")
    print(results.tojson(normalize=False))
    name=json.loads(results.tojson(normalize=False))
    try:
        print(name[0]["name"])
        return name[0]["name"],name
    except:
        return "no detection"
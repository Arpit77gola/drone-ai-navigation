import torch
import cv2

# Load YOLOv5 model (small version)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', source='github')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    results = model(frame)

    # Plot detection results
    frame = results.render()[0]

    cv2.imshow('YOLOv5 Detection - Press Q to Quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

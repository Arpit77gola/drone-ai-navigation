import torch
import cv2
import urllib.request
import os
import numpy as np
from gpt_explainer import explain_decision


# Load MiDaS model
model_type = "MiDaS_small"  # lightweight model
midas = torch.hub.load("intel-isl/MiDaS", model_type)

# Load transforms to prepare image
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.small_transform

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
midas.to(device)
midas.eval()

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_batch = transform(img).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()
    
    # Normalize for display
    depth_min = depth_map.min()
    depth_max = depth_map.max()
    depth_map = (depth_map - depth_min) / (depth_max - depth_min)
    depth_map = (depth_map * 255).astype(np.uint8)

    depth_map_color = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)

    cv2.imshow("Depth Map", depth_map_color)
    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

from navigation_logic import get_navigation_decision
# Normalize
depth_min = depth_map.min()
depth_max = depth_map.max()
depth_map = (depth_map - depth_min) / (depth_max - depth_min)
depth_map = np.clip(depth_map, 0, 1)

# 👉 Get navigation command
import pyttsx3
command, avg_depth = get_navigation_decision(depth_map)
print("Drone Decision:", command)

explanation = explain_decision(avg_depth, command)
print("GPT Explanation:", explanation)

# Speak the explanation
engine = pyttsx3.init()
try:
    engine.say(explanation)
    engine.runAndWait()
except RuntimeError:
    pass  # Prevents the "run loop already started" error




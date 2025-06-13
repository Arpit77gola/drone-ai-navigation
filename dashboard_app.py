import streamlit as st
import cv2
import numpy as np
from navigation_logic import get_navigation_decision
from gpt_explainer import explain_decision
import pyttsx3

if "stop_loop" not in st.session_state:
    st.session_state.stop_loop = False
if "stop_button_clicked" not in st.session_state:
    st.session_state.stop_button_clicked = False




st.set_page_config(page_title="Drone AI Dashboard", layout="centered")

st.title("🛸 Drone AI Navigation Dashboard")

# Webcam frame capture
frame_window = st.image([])
depth_window = st.image([])

start = st.button("Start Drone")


if start:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    engine = pyttsx3.init()
    voice_enabled = st.checkbox("🔊 Voice Output", value=True)

    stop = False

    while cap.isOpened() and not st.session_state.stop_loop:

        # All the remaining block (frame read, RGB conversion, logic, etc.)
        ...

        ret, frame = cap.read()
        if not ret:
            st.error("Camera not found")
            break

        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Dummy depth map for demo (replace with MiDaS logic)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        depth_map = cv2.applyColorMap(gray, cv2.COLORMAP_MAGMA)

        # Create fake normalized map (simulate MiDaS)
        norm_map = gray / 255.0
        command, avg_depth = get_navigation_decision(norm_map)
        explanation = explain_decision(avg_depth, command)

        st.markdown(f"### 🤖 Decision: {command}")
        st.markdown(f"**🧠 Explanation:** {explanation}")

        engine.say(explanation)
        engine.runAndWait()

        frame_window.image(rgb, channels="RGB")
        depth_window.image(depth_map, channels="BGR")

        if not st.session_state.stop_button_clicked:
          if st.button("🛑 Stop", key="stop_button_unique"):  # 🔑 Use unique key
            st.session_state.stop_loop = True
          st.session_state.stop_button_clicked = True
        break



    cap.release()
st.session_state.stop_loop = False
st.session_state.stop_button_clicked = False


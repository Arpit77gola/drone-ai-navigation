def explain_decision(depth_value, action):
    if action == "STOP 🚫":
        return f"The drone detected a very close obstacle at {round(depth_value * 2.5, 2)} meters and stopped to avoid collision."
    elif action == "TURN LEFT ⬅️":
        return f"An obstacle was detected within {round(depth_value * 2.5, 2)} meters, so the drone turned left for safety."
    else:
        return f"The area ahead is clear with an average distance of {round(depth_value * 2.5, 2)} meters, so the drone moved forward."

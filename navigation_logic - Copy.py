import numpy as np


def get_navigation_decision(depth_map, threshold=0.3):
    h, w = depth_map.shape
    center = depth_map[h//3:2*h//3, w//3:2*w//3]
    avg_depth = np.mean(center)
    print("Average Center Depth:", round(avg_depth, 2))

    if avg_depth < threshold * 0.5:
        decision = "STOP 🚫"
    elif avg_depth < threshold:
        decision = "TURN LEFT ⬅️"
    else:
        decision = "GO FORWARD ➡️"
    
    return decision, avg_depth

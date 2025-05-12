import cv2
import numpy as np

# video 
cam = 0  
cap = cv2.VideoCapture(cam)

if not cap.isOpened():
    print("Error: Unable to connect to the mobile camera.")
    exit(1)

# Function to determine the water color level
def get_water_level(color_bgr):
    color_ranges = [
        {
            "level": "Level 1: Light Yellow", 
            "min": np.array([255, 223, 200]), 
            "max": np.array([255, 255, 255])
        },
        {
            "level": "Level 2: Dark Yellow", 
            "min": np.array([225, 175, 90]), 
            "max": np.array([255, 225, 120])
        },
        {
            "level": "Level 3: Yellowish Brown", 
            "min": np.array([153, 102, 51]), 
            "max": np.array([200, 150, 75])
        },
        {
            "level": "Level 4: Dark Brown", 
            "min": np.array([102, 51, 25]), 
            "max": np.array([150, 100, 50])
        },
        {
            "level": "Level 5: Almost Black Brown", 
            "min": np.array([51, 25, 0]), 
            "max": np.array([100, 50, 25])
        }
    ]
    for color_range in color_ranges:
        if np.all(color_bgr >= color_range["min"]) and np.all(color_bgr <= color_range["max"]):
            return color_range["level"]
    return "Unknown Level"

# Main loop
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame from the camera")
        break

    frame_height, frame_width = frame.shape[:2]
    box_size = 5
    grid_size = 3
    spacing = 2 * box_size + 5

    start_x = frame_width // 2 - spacing
    start_y = frame_height // 2 - spacing

    results = []

    for row in range(grid_size):
        for col in range(grid_size):
            cx = start_x + col * spacing
            cy = start_y + row * spacing

            x1, y1 = max(0, cx - box_size), max(0, cy - box_size)
            x2, y2 = min(frame_width, cx + box_size), min(frame_height, cy + box_size)

            roi = frame[y1:y2, x1:x2]
            avg_color = np.mean(roi, axis=(0, 1)).astype(np.uint8)

            level = get_water_level(avg_color)
            results.append(f"({row},{col}): {level}")

            # Draw only the rectangle, no text inside
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

    # Show all results at the top-left
    for i, text in enumerate(results):
        cv2.putText(frame, text, (10, 20 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Display the frame
    cv2.imshow("Mobile Camera - 3x3 Water Level", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

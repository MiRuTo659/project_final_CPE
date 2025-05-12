import cv2
import numpy as np

# Load image from file
image_path = 'detectcolorriver/img/pic_1.jpg'
frame = cv2.imread(image_path)
frame = cv2.resize(frame, (640, 480))

if frame is None:
    print("Error: Unable to load the image.")
    exit(1)

def get_water_level(color_bgr):
    color_ranges = [
        {
            "level": "Level 1: Light Yellow", 
            "min": np.array([220, 220, 170]), 
            "max": np.array([255, 255, 210])
        },
        {
            "level": "Level 2: Dark Yellow", 
            "min": np.array([180, 180, 90]), 
            "max": np.array([230, 230, 150])
        },
        {
            "level": "Level 3: Yellowish Brown", 
            "min": np.array([130, 100, 50]), 
            "max": np.array([180, 150, 100])
        },
        {
            "level": "Level 4: Dark Brown", 
            "min": np.array([80, 50, 20]), 
            "max": np.array([130, 100, 60])
        },
        {
            "level": "Level 5: Almost Black Brown", 
            "min": np.array([30, 20, 0]), 
            "max": np.array([80, 50, 30])
        }
    ]
    for color_range in color_ranges:
        if np.all(color_bgr >= color_range["min"]) and np.all(color_bgr <= color_range["max"]):
            return color_range["level"]
    return "Unknown Level"

frame_height, frame_width = frame.shape[:2]
box_size = 10  # Half of box width
grid_size = 3
spacing = 2 * box_size + 5

start_x = frame_width // 2 - spacing
start_y = frame_height // 2 - spacing

results = []  # Store results of each box

for row in range(grid_size):
    for col in range(grid_size):
        cx = start_x + col * spacing
        cy = start_y + row * spacing
        x1, y1 = max(0, cx - box_size), max(0, cy - box_size)
        x2, y2 = min(frame_width, cx + box_size), min(frame_height, cy + box_size)

        roi = frame[y1:y2, x1:x2]
        avg_color = np.mean(roi, axis=(0, 1)).astype(np.uint8)
        level = get_water_level(avg_color)

        # Draw the box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        # Add to result list
        results.append(f"({row},{col}): {level}")

# Display all levels at top-left corner
start_text_y = 20
for i, text in enumerate(results):
    cv2.putText(frame, text, (10, start_text_y + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

cv2.imshow("3x3 Grid Water Levels", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

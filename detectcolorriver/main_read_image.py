import cv2
import numpy as np

# Load image from file (replace with the path to your image)
image_path = 'detectcolorriver/img/pic_1.jpg'
frame = cv2.imread(image_path)

frame = cv2.resize(frame, (640, 480))

if frame is None:
    print("Error: Unable to load the image.")
    exit(1)

# Function to determine the water color level
def get_water_level(color_bgr):
    # Define the color ranges for each level (BGR format)
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

    # Compare the color with the defined ranges
    for color_range in color_ranges:
        if np.all(color_bgr >= color_range["min"]) and np.all(color_bgr <= color_range["max"]):
            return color_range["level"]
    return "Unknown Level"  # In case it doesn't match any range

# Calculate the center of the image
frame_width, frame_height = frame.shape[1], frame.shape[0]
center_x, center_y = frame_width // 2, frame_height // 2

# Define the size of the box
box_size = 13  # Increased size for averaging over a larger area

# Calculate the position of the box
x1, y1 = center_x - box_size, center_y - box_size
x2, y2 = center_x + box_size, center_y + box_size

# Crop the box to stay within the frame boundaries
x1 = max(0, x1)
y1 = max(0, y1)
x2 = min(frame_width, x2)
y2 = min(frame_height, y2)

# Crop the region of interest (ROI) for averaging
roi = frame[y1:y2, x1:x2]

# Calculate the average color of the ROI (region of interest)
average_color = np.mean(roi, axis=(0, 1)).astype(np.uint8)
print("Average BGR color:", average_color)

# Determine the water level based on the average color
water_level = get_water_level(average_color)

# Display the result on the image
cv2.putText(frame, water_level, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Create a box around the center position
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the image
cv2.imshow("Image", frame)

# Wait for any key press to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

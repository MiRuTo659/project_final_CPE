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
    # Define the color ranges for each level (BGR format)
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

    # Compare the color with the defined ranges
    for color_range in color_ranges:
        if np.all(color_bgr >= color_range["min"]) and np.all(color_bgr <= color_range["max"]):
            return color_range["level"]
    return "Unknown Level"  # In case it doesn't match any range

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame from the camera")
        break

    # Calculate the center of the frame
    frame_width, frame_height = frame.shape[1], frame.shape[0]
    center_x, center_y = frame_width // 2, frame_height // 2

    # Define the size of the box
    box_size = 3  # Adjust the size as needed

    # Calculate the position of the box
    x1, y1 = center_x - box_size, center_y - box_size
    x2, y2 = center_x + box_size, center_y + box_size

    # Crop the box to stay within the frame boundaries
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(frame_width, x2)
    y2 = min(frame_height, y2)

    # Read the color at the center of the frame
    color_bgr = frame[center_y, center_x]

    # Determine the water level based on the color
    water_level = get_water_level(color_bgr)

    # Display the result on the image
    cv2.putText(frame, water_level, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Create a box around the center position
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the camera frame
    cv2.imshow("Mobile Camera", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release() # video
cv2.destroyAllWindows()

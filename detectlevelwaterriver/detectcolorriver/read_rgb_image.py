import cv2
import numpy as np

# Load image from file (replace with the path to your image)
image_path = 'detectcolorriver/img/pic_1.jpg'
frame = cv2.imread(image_path)

if frame is None:
    print("Error: Unable to load the image.")
    exit(1)

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

# Convert BGR to RGB
color_rgb = color_bgr[::-1]
print("RGB Color:", color_rgb)

# Display BGR color
print("BGR Color:", color_bgr)

# Create a box around the center position
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the image
cv2.imshow("Image", frame)

# Wait for any key press to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

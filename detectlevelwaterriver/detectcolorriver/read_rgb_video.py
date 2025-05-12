import cv2
import numpy as np

# Replace the following line with the IPv4 address of your mobile camera
ip_camera_url = 0

# Open the mobile camera feed
cap = cv2.VideoCapture(ip_camera_url)

if not cap.isOpened():
    print("Error: Unable to connect to the mobile camera.")
    exit(1)

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

    # Convert BGR to RGB
    color_rgb = color_bgr[::-1]
    print("RGB Color:", color_rgb)

    # Display BGR color
    print("BGR Color:", color_bgr)

    # Create a box around the center position
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the camera frame
    cv2.imshow("Mobile Camera", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np

def nothing(x):
    pass

def rgb_calc():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Trackbars")

    # Create RGB trackbars
    cv2.createTrackbar("lr", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("lg", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("lb", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("ur", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("ug", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("ub", "Trackbars", 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get RGB values from trackbars
        lr = cv2.getTrackbarPos("lr", "Trackbars")
        lg = cv2.getTrackbarPos("lg", "Trackbars")
        lb = cv2.getTrackbarPos("lb", "Trackbars")
        ur = cv2.getTrackbarPos("ur", "Trackbars")
        ug = cv2.getTrackbarPos("ug", "Trackbars")
        ub = cv2.getTrackbarPos("ub", "Trackbars")

        # Lower and upper bounds in BGR (OpenCV uses BGR)
        lower = np.array([lb, lg, lr])
        upper = np.array([ub, ug, ur])

        # Create mask and result
        mask = cv2.inRange(frame, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Show windows
        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Filtered Result", result)

        key = cv2.waitKey(1)
        if key == 27: # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

rgb_calc()

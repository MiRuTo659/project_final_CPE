import cv2
import numpy as np

def detect_water_height(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    levels = {
        "High Water Level": int(height * 0.6),
        "Medium Water Level": int(height * 0.7),
        "Low Water Level": int(height * 0.8)
    }

    lower_brown = np.array([5, 50, 50])
    upper_brown = np.array([30, 255, 255])

    current_level = "Below Low Water Level"
    for label, y in sorted(levels.items(), key=lambda x: x[1], reverse=True):
        line = hsv[y:y+1, :, :]
        mask = cv2.inRange(line, lower_brown, upper_brown)
        water_pixels = np.sum(mask > 0)
        if water_pixels > width * 0.5:
            current_level = label
            break

    return levels, current_level

def get_water_level_from_color(color_bgr):
    color_ranges = [
        {"level": "Level 1: Light Yellow", "min": np.array([220, 220, 170]), "max": np.array([255, 255, 210])},
        {"level": "Level 2: Dark Yellow", "min": np.array([180, 180, 90]), "max": np.array([230, 230, 150])},
        {"level": "Level 3: Yellowish Brown", "min": np.array([130, 100, 50]), "max": np.array([180, 150, 100])},
        {"level": "Level 4: Dark Brown", "min": np.array([80, 50, 20]), "max": np.array([130, 100, 60])},
        {"level": "Level 5: Almost Black Brown", "min": np.array([30, 20, 0]), "max": np.array([80, 50, 30])}
    ]
    for color_range in color_ranges:
        if np.all(color_bgr >= color_range["min"]) and np.all(color_bgr <= color_range["max"]):
            return color_range["level"]
    return "Unknown Level"

def analyze_3x3_color_grid(frame):
    h, w = frame.shape[:2]
    box_size = 10
    grid_size = 3
    spacing = 2 * box_size + 5
    start_x = w // 2 - spacing
    start_y = h // 2 - spacing

    results = []
    for row in range(grid_size):
        for col in range(grid_size):
            cx = start_x + col * spacing
            cy = start_y + row * spacing
            x1, y1 = max(0, cx - box_size), max(0, cy - box_size)
            x2, y2 = min(w, cx + box_size), min(h, cy + box_size)

            roi = frame[y1:y2, x1:x2]
            avg_color = np.mean(roi, axis=(0, 1)).astype(np.uint8)
            level = get_water_level_from_color(avg_color)
            results.append(((x1, y1, x2, y2), f"({row},{col}): {level}"))
    return results

# === เปิดกล้อง ===
cap = cv2.VideoCapture("rtsp://192.168.137.61/stream/0")  # หากมีหลายกล้อง ลองเปลี่ยนเลขเป็น 1, 2

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถอ่านภาพจากกล้อง")
        break

    frame_real = cv2.resize(frame, (1920, 1080))
    frame = cv2.flip(frame_real, 1)
    levels, current_level = detect_water_height(frame)
    grid_results = analyze_3x3_color_grid(frame)
    output = frame.copy()
    height, width = output.shape[:2]

    # วาดเส้นระดับน้ำ
    for label, y in levels.items():
        color = (0, 0, 255) if "High" in label else (0, 165, 255) if "Medium" in label else (0, 255, 0)
        cv2.line(output, (0, y), (width, y), color, 2)
        cv2.putText(output, label, (10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # แสดงผลระดับน้ำปัจจุบัน
    cv2.putText(output, f"Current Water Level: {current_level}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # วาดกรอบ 3x3 และผลลัพธ์สี
    text_y = 60
    for (x1, y1, x2, y2), text in grid_results:
        cv2.rectangle(output, (x1, y1), (x2, y2), (255, 255, 0), 1)
        cv2.putText(output, text, (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        text_y += 20

    # แสดงภาพ
    cv2.imshow("Real-Time Water Level Detection", output)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # กด s เพื่อบันทึกภาพ
        cv2.imwrite("water_level_live_capture.jpg", output)
        print("📸 บันทึกภาพไว้ที่ water_level_live_capture.jpg")

cap.release()
cv2.destroyAllWindows()

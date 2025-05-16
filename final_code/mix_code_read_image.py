import cv2
import numpy as np
import os

# ==== ตรวจจับระดับน้ำตามความสูงของภาพ ====
def detect_water_height(cv_image):
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    height, width, _ = cv_image.shape

    levels = {
        "High Water Level": int(height * 0.6),
        "Medium Water Level": int(height * 0.7),
        "Low Water Level": int(height * 0.8)
    }

    # ปรับค่า HSV สำหรับน้ำสีน้ำตาล (ต้องปรับตามภาพจริง)
    lower_brown = np.array([5, 50, 50])
    upper_brown = np.array([30, 255, 255])

    current_level = "Below Low Water Level"
    for label, y in sorted(levels.items(), key=lambda x: x[1], reverse=True):
        line = hsv[y:y+1, :, :]
        mask = cv2.inRange(line, lower_brown, upper_brown)
        water_pixels = np.sum(mask > 0)

        print(f"{label} at y={y} has {water_pixels} brown pixels")  # Debug

        if water_pixels > width * 0.5:
            current_level = label
            break

    return levels, current_level

# ==== วิเคราะห์สีของน้ำใน 3x3 จุด ====
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
            print(f"Grid ({row},{col}) avg_color: {avg_color}, level: {level}")  # Debug
            results.append(((x1, y1, x2, y2), f"({row},{col}): {level}"))
    return results

# ==== MAIN PROGRAM ====
image_path = r"detectcolorriver\img\pic_3.jpg"
cv_image = cv2.imread(image_path)

if cv_image is None:
    print("ไม่สามารถโหลดภาพได้")
    exit(1)

# === Resize image to standard size (adjust as needed) ===
cv_image = cv2.resize(cv_image, (720, 720))

levels, current_level = detect_water_height(cv_image)
grid_results = analyze_3x3_color_grid(cv_image)
output_img = cv_image.copy()
height, width = output_img.shape[:2]

# วาดเส้นระดับน้ำ
for label, y in levels.items():
    color = (0, 0, 255) if "High" in label else (0, 165, 255) if "Medium" in label else (0, 255, 0)
    cv2.line(output_img, (0, y), (width, y), color, 2)
    cv2.putText(output_img, label, (10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# แสดงผลระดับน้ำปัจจุบัน
cv2.putText(output_img, f"Current Water Level: {current_level}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# วาดกรอบ 3x3 และแสดงผลสี
text_y = 60
for (x1, y1, x2, y2), text in grid_results:
    cv2.rectangle(output_img, (x1, y1), (x2, y2), (255, 255, 0), 1)
    cv2.putText(output_img, text, (10, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    text_y += 20

# สร้างโฟลเดอร์หากยังไม่มี
output_dir = "detectlevelwaterriver/image_detect_level_river"
os.makedirs(output_dir, exist_ok=True)

# แสดงภาพและบันทึก
cv2.imshow("Water Level and Color Analysis", output_img)
cv2.imwrite(os.path.join(output_dir, "water_level.jpg"), output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"ระดับน้ำที่ตรวจพบ: {current_level}")

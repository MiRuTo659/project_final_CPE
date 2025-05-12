from PIL import Image, ImageDraw
import cv2
import numpy as np

# โหลดภาพด้วย OpenCV
image_path = "detectcolorriver\\img\\pic_2.jpg"
cv_image = cv2.imread(image_path)
hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

height, width, _ = cv_image.shape

# นิยามระดับน้ำ (จากด้านบนลงล่าง)
levels = {
    "High Water Level": int(height * 0.6),
    "Medium Water Level": int(height * 0.7),
    "Low Water Level": int(height * 0.8)
}

# กำหนดช่วงสีน้ำตาล (น้ำแม่น้ำ)
lower_brown = np.array([5, 50, 50])
upper_brown = np.array([30, 255, 255])

# ตรวจสอบระดับน้ำจากล่างขึ้นบน
current_level = "Below Low Water Level"
for label, y in sorted(levels.items(), key=lambda x: x[1], reverse=True):
    # ตัดแถว Y เป็นแนวนอน (แนวระดับเดียว)
    line = hsv[y:y+1, :, :]
    mask = cv2.inRange(line, lower_brown, upper_brown)
    
    water_pixels = np.sum(mask > 0)
    if water_pixels > width * 0.5:  # ถ้ามากกว่า 50% ของแนวกว้างเป็นน้ำ
        current_level = label
        break

# แปลง OpenCV image (BGR) → PIL image (RGB)
cv_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(cv_rgb)

# วาดเส้นระดับน้ำด้วย PIL
draw = ImageDraw.Draw(pil_image)
for label, y in levels.items():
    color = "red" if "High" in label else ("orange" if "Medium" in label else "green")
    draw.line([(0, y), (width, y)], fill=color, width=2)
    draw.text((10, y - 20), label, fill=color)

# วาดข้อความแสดงระดับน้ำปัจจุบัน
draw.text((20, 20), f"Current Water Level: {current_level}", fill="red")

# บันทึกภาพ
output_path = "detectlevelwaterriver\\image_detect_level_river\\test_water_levels_detected.jpg"
pil_image.save(output_path)
pil_image.show()

print(f"ตรวจพบระดับน้ำที่: {current_level}")

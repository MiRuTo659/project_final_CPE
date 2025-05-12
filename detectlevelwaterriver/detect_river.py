import cv2
import numpy as np
from PIL import Image

# โหลดภาพ
image_path = "detectcolorriver\img\pic_2.jpg"  # เปลี่ยนเป็น path ของไฟล์ภาพคุณ
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# แปลงภาพเป็นสี HSV เพื่อกรองเฉดสีน้ำ
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# กำหนดช่วงสีที่สื่อถึงน้ำ (น้ำตาล/น้ำขุ่น)
lower_brown = np.array([5, 50, 50])
upper_brown = np.array([30, 255, 255])

# สร้าง mask เพื่อแยกพื้นที่น้ำ
mask = cv2.inRange(hsv, lower_brown, upper_brown)

# ทำความสะอาด mask ด้วย Morphological operations
kernel = np.ones((5, 5), np.uint8)
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel)

# หา Contours
contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# วาดเส้นขอบลงบนภาพเดิม
contour_image = image_rgb.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)  # สีเขียว

# บันทึกหรือแสดงผลภาพ
output = Image.fromarray(contour_image)
output.save("detectlevelwaterriver\image_detect_color\detect_water_river_2.jpg")
output.show()

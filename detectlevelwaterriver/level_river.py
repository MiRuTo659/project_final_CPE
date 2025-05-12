from PIL import Image, ImageDraw

# โหลดภาพ
image_path = "detectcolorriver\img\pic_2.jpg"  # เปลี่ยนชื่อไฟล์ตามจริง
image = Image.open(image_path)
width, height = image.size

# นิยามระดับน้ำที่ต้องการ (จากด้านบน)
levels = {
    "High Water Level": int(height * 0.2),   # 20% จากด้านบน
    "Medium Water Level": int(height * 0.5), # 50%
    "Low Water Level": int(height * 0.8)     # 80%
}

# วาดเส้นระดับน้ำ
draw = ImageDraw.Draw(image)
for label, y in levels.items():
    color = "red" if "High" in label else ("orange" if "Medium" in label else "green")
    draw.line([(0, y), (width, y)], fill=color, width=2)
    draw.text((10, y - 20), label, fill=color)

# บันทึกผลลัพธ์
output_path = "detectlevelwaterriver\image_detect_level_river\water_levels_only.jpg"
image.save(output_path)
image.show()
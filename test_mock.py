import os
import time
from PIL import Image, ImageDraw, ImageFont

def mock_ai_generate_content(topic: str) -> str:
    """1. จำลอง AI คิดเนื้อหาคอนเทนต์"""
    print(f"🤖 [จำลอง] AI กำลังประมวลผลหัวข้อ: '{topic}'...")
    time.sleep(2) # จำลองเวลาที่ AI ใช้คิด
    
    content = f"""🚀 5 เทคนิคเปลี่ยนชีวิตด้วย: {topic}

ยุคนี้ใครๆ ก็พูดถึงการทำงานให้ไวขึ้น! วันนี้เรามาดูวิธีเริ่มง่ายๆ กันครับ:

1️⃣ ใช้ Tool ช่วยเรียงความสำคัญงาน
2️⃣ สรุปประชุมสั้นลง 50%
3️⃣ จัดตารางเวลาแบบ Time-boxing
4️⃣ พักสายตา 5 นาทีทุกๆ ชั่วโมง
5️⃣ นำ AI มาช่วยร่างไอเดียเบื้องต้น

เพื่อนๆ ชอบข้อไหนกันบ้าง? คอมเมนต์บอกกันหน่อยครับ! 👇

#AIAutomation #Productivity #WorkSmart #เทคนิคการทำงาน #{topic.replace(' ', '')}"""
    return content

def mock_generate_image(text: str, filename: str = "mock_banner.png"):
    """2. จำลองการสร้างรูปภาพประกอบโพสต์"""
    print("🎨 [จำลอง] กำลังสร้างรูปภาพประกอบ...")
    
    # สร้างรูปภาพขนาด 1080x1080 (ขนาดภาพ Square บน FB)
    img = Image.new('RGB', (1080, 1080), color=(24, 119, 242)) # สีฟ้า Facebook
    draw = ImageDraw.Draw(img)
    
    # วาดกรอบตกแต่ง
    draw.rectangle([50, 50, 1030, 1030], outline=(255, 255, 255), width=8)
    
    # บันทึกรูปภาพลงโฟลเดอร์โปรเจกต์
    img.save(filename)
    print(f"📸 สร้างรูปภาพจำลองสำเร็จ: {filename}")
    return filename

def generate_html_preview(content: str, image_path: str):
    """3. จำลองการโพสต์ FB โดยสร้างไฟล์ HTML ดูตัวอย่างในเบราว์เซอร์"""
    print("🌐 [จำลอง] กำลังสร้างหน้าพรีวิวเหมือนหน้า Facebook จริง...")
    
    formatted_content = content.replace('\n', '<br>')
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>Facebook Post Preview</title>
        <style>
            body {{ font-family: sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; padding: 20px; }}
            .card {{ background: white; width: 500px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 16px; }}
            .header {{ display: flex; align-items: center; margin-bottom: 12px; }}
            .avatar {{ width: 40px; height: 40px; border-radius: 50%; background: #1877f2; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px; }}
            .page-name {{ font-weight: bold; font-size: 15px; }}
            .time {{ font-size: 12px; color: gray; }}
            .content {{ font-size: 14px; line-height: 1.5; margin-bottom: 12px; }}
            .post-img {{ width: 100%; border-radius: 6px; }}
            .badge {{ background: #e4e6eb; padding: 4px 8px; border-radius: 4px; font-size: 12px; color: #050505; font-weight: bold; display: inline-block; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div>
            <div class="badge">⚠️ โหมดทดสอบจำลอง (Mock System)</div>
            <div class="card">
                <div class="header">
                    <div class="avatar">FB</div>
                    <div>
                        <div class="page-name">My AI Automation Page</div>
                        <div class="time">เมื่อสักครู่นี้ · 🌎</div>
                    </div>
                </div>
                <div class="content">{formatted_content}</div>
                <img class="post-img" src="{image_path}" alt="Post Banner">
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    
    print("\n✅ ทดสอบระบบสำเร็จ 100%!")
    print("👉 เปิดไฟล์ 'preview.html' ในโฟลเดอร์ เพื่อดูผลลัพธ์จำลองได้เลยครับ")

if __name__ == "__main__":
    # หัวข้อทดสอบ
    topic = "การบริหารเวลา"
    
    # รัน Flow การทำงานจำลอง
    caption = mock_ai_generate_content(topic)
    img_file = mock_generate_image(topic)
    generate_html_preview(caption, img_file)
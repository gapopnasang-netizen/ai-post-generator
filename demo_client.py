import os
import time
import requests
import urllib.parse

def generate_ai_content_demo(topic: str, style_type: int) -> tuple[str, str]:
    """1. สร้างเนื้อหาตามสไตล์ที่เลือก + คืนค่า Image Prompt สำหรับสร้างภาพ"""
    print(f"\n🧠 [AI Engine] กำลังประมวลผลบทความหัวข้อ: '{topic}'...")
    time.sleep(1.5) # จำลองเวลาประมวลผล
    
    if style_type == 1: # แนวความรู้ / สรุปประเด็น
        content = f"""💡 **[สาระน่ารู้] {topic} ที่คนทำงานยุคนี้ต้องรู้!**

เคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงกลายเป็นสิ่งที่ทุกคนกำลังพูดถึง?

วันนี้เราย่อย 3 หัวใจสำคัญมาให้แล้วครับ 👇

🔹 **1. จุดเริ่มต้น:** เข้าใจพื้นฐานเพื่อนำไปปรับใช้ได้จริง
🔹 **2. เครื่องมือที่ช่วยได้:** ประหยัดเวลาทำงานลงมากกว่า 50%
🔹 **3. ผลลัพธ์ที่ได้:** เพิ่มประสิทธิภาพอย่างเห็นได้ชัด

ลองนำไปปรับใช้ในชีวิตประจำวันดูนะครับ! เพื่อนๆ มีความคิดเห็นอย่างไรกับเรื่องนี้ คอมเมนต์คุยกันได้เลยครับ 👇

#สาระน่ารู้ #Productivity #เทคโนโลยี #{topic.replace(' ', '')}"""
        image_prompt = f"Professional high quality graphic illustration of {topic}, modern tech aesthetic, clean design, 8k resolution"

    elif style_type == 2: # แนวขายสินค้า / โปรโมชัน
        content = f"""🔥 **PROMOTION พิเศษ! ยกระดับ {topic} ของคุณวันนี้** 🔥

คุณกำลังเจอ ปัญหาเหล่านี้อยู่ใช่ไหม? 
ยุ่งยาก ใช้เวลานาน และไม่ได้ผลลัพธ์ตามที่ต้องการ...

✨ **ขอแนะนำโซลูชันที่จะเปลี่ยนชีวิตคุณ:**
✅ ประหยัดเวลาทำงานขึ้น 3 เท่า
✅ ใช้งานง่าย ไม่ซับซ้อน
✅ คุ้มค่า ตอบโจทย์ทุกการใช้งาน

🎁 **ข้อเสนอพิเศษเฉพาะสัปดาห์นี้เท่านั้น!**
ทักแชตเพจ รับส่วนลดพิเศษทันที 20% 📩

#โปรโมชันพิเศษ #สินค้าแนะนำ #{topic.replace(' ', '')} #คุ้มค่า"""
        image_prompt = f"3D render commercial product photography style for {topic}, vibrant colors, high contrast, studio lighting, highly detailed"

    else: # แนวเล่าเรื่อง / แรงบันดาลใจ
        content = f"""🌟 **เรื่องราวเปลี่ยนชีวิต: จากจุดเริ่มต้นสู่ความสำเร็จในเรื่อง {topic}**

"ถ้าไม่เริ่มวันนี้ วันข้างหน้าเราก็ยังยืนอยู่ที่เดิม"

หลายคนถามเข้ามาเยอะมากเกี่ยวกับการเริ่มทำ '{topic}' 
ข้อคิดสำคัญที่สุดที่เราได้เรียนรู้ตลอดช่วงที่ผ่านมาคือ:

1. ไม่ต้องรอให้พร้อม 100% ค่อยเริ่ม
2. ความสม่ำเสมอสำคัญกว่าความสมบูรณ์แบบ
3. เรียนรู้จากข้อผิดพลาด แล้วปรับปรุงให้ไวขึ้น

ขอเป็นกำลังใจให้ทุกคนที่กำลังพัฒนาตัวเองอยู่นะครับ 💪💙

#แรงบันดาลใจ #ข้อคิดดีๆ #ข้อคิดพัฒนาตนเอง #{topic.replace(' ', '')}"""
        image_prompt = f"Cinematic atmospheric photography, inspiring motivation concept for {topic}, warm golden hour lighting, masterpiece"

    return content, image_prompt

def generate_real_ai_image(image_prompt: str, output_filename: str = "demo_ai_image.jpg") -> str:
    """2. เจนภาพ AI ของจริงด้วย FLUX Model (ฟรี ไม่ต้องใช้ API Key)"""
    print(f"🎨 [FLUX AI] กำลังเจนรูปภาพจริงจาก Prompt: '{image_prompt[:50]}...'")
    
    # แปลงข้อความให้รองรับ URL Format
    encoded_prompt = urllib.parse.quote(image_prompt)
    
    # URL สำหรับดึงภาพจาก FLUX Model (ขนาด 1080x1080 เท่ากับภาพบน Facebook)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux&nologo=true"
    
    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ บันทึกรูปภาพ AI จริงเรียบร้อย: {output_filename}")
            return output_filename
        else:
            print("❌ ไม่สามารถดึงรูปภาพได้ ใช้ภาพสำรองแทน")
            return None
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการสร้างรูปภาพ: {e}")
        return None

def make_client_preview(content: str, image_path: str):
    """3. สร้างหน้าพรีวิวสวยๆ ให้ลูกค้าดูแบบเรียลไทม์"""
    formatted_content = content.replace('\n', '<br>')
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>Facebook Post Demo Preview</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; padding: 30px; margin: 0; }}
            .preview-container {{ width: 500px; }}
            .demo-badge {{ background: #1877f2; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; text-align: center; margin-bottom: 15px; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .card {{ background: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); padding: 16px; border: 1px solid #e0e0e0; }}
            .header {{ display: flex; align-items: center; margin-bottom: 12px; }}
            .avatar {{ width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(45deg, #1877f2, #00c6ff); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; margin-right: 10px; }}
            .page-name {{ font-weight: 600; font-size: 15px; color: #050505; }}
            .time {{ font-size: 12px; color: #65676b; margin-top: 2px; }}
            .content {{ font-size: 15px; line-height: 1.6; color: #050505; margin-bottom: 14px; white-space: pre-wrap; }}
            .post-img {{ width: 100%; border-radius: 8px; object-fit: cover; max-height: 500px; }}
            .footer-actions {{ display: flex; justify-content: space-around; border-top: 1px solid #e4e6eb; margin-top: 12px; padding-top: 8px; font-size: 14px; color: #65676b; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="preview-container">
            <div class="demo-badge">✨ AI Automation Post Preview (สำหรับนำเสนอลูกค้า)</div>
            <div class="card">
                <div class="header">
                    <div class="avatar">AI</div>
                    <div>
                        <div class="page-name">Demo Brand Official</div>
                        <div class="time">เมื่อสักครู่นี้ · 🌎 โพสต์โดยระบบอัตโนมัติ</div>
                    </div>
                </div>
                <div class="content">{content}</div>
                <img class="post-img" src="{image_path}" alt="AI Generated Banner">
                <div class="footer-actions">
                    <span>👍 ถูกใจ</span>
                    <span>💬 แสดงความคิดเห็น</span>
                    <span>↪️ แชร์</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("client_preview.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("\n🎉 พรีวิวสำหรับลูกค้าเสร็จแล้ว! เปิดไฟล์ 'client_preview.html' ได้เลยครับ")

if __name__ == "__main__":
    print("==========================================")
    print("   🤖 ระบบจำลอง AI Automation สำหรับ Demo")
    print("==========================================")
    
    # 1. รับค่าหัวข้อจากคุณ
    user_topic = input("\n👉 กรอกหัวข้อที่ต้องการ Demo (เช่น กาแฟโบราณ, อาหารเสริม, AI ช่วยทำงาน): ") or "การใช้นวัตกรรม AI ในธุรกิจ"
    
    # 2. เลือกสไตล์โพสต์
    print("\nเลือกสไตล์โพสต์:")
    print("1. แนวให้ความรู้ / สรุปสาระ (Educational)")
    print("2. แนวขายสินค้า / โปรโมชัน (Sales & Promo)")
    print("3. แนวเล่าเรื่อง / แรงบันดาลใจ (Storytelling)")
    style_choice = int(input("พิมพ์หมายเลข (1-3): ") or 1)
    
    # 3. รันระบบสร้างโพสต์ + เจนภาพ AI
    caption, img_prompt = generate_ai_content_demo(user_topic, style_choice)
    img_filename = generate_real_ai_image(img_prompt)
    
    # 4. สร้างไฟล์ Preview
    if img_filename:
        make_client_preview(caption, img_filename)
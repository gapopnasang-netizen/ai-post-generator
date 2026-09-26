import os
import requests
from dotenv import load_dotenv
import anthropic

# โหลด API Keys จากไฟล์ .env
load_dotenv()

CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

# เรียกใช้ Claude Client
client = anthropic.Anthropic(api_key=CLAUDE_KEY)

def generate_content(topic: str) -> str:
    print(f"🤖 กำลังให้ Claude คิดคอนเทนต์เรื่อง: '{topic}'...\n")
    
    prompt = f"""
    ช่วยเขียนโพสต์ Facebook สำหรับเพจในหัวข้อ: '{topic}'
    - มีหัวข้อที่น่าสนใจ ดึงดูดสายตา
    - เนื้อหาอ่านง่าย สั้นกระชับ
    - ใช้อีโมจิประกอบ
    - ใส่ Hashtag 3-5 อันท้ายโพสต์
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    # ใส่หัวข้อคอนเทนต์ที่ต้องการทดสอบ
    topic = "เทคนิคการบริหารเวลาสำหรับคนทำงานยุค AI"
    
    try:
        content = generate_content(topic)
        print("--- ผลลัพธ์คอนเทนต์ ---")
        print(content)
        print("--------------------")
    except Exception as e:
        print("❌ เกิดข้อผิดพลาด:", e)
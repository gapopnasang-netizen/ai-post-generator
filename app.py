import streamlit as st
import requests
import urllib.parse
import random
import time

# 1. ตั้งค่าหน้าตาเว็บ
st.set_page_config(
    page_title="AI Social Content Studio",
    page_icon="🚀",
    layout="wide"
)

# 2. เมนู Sidebar
with st.sidebar:
    st.title("⚙️ ตั้งค่าระบบ")
    style_option = st.selectbox(
        "🎨 สไตล์คอนเทนต์:",
        [
            "1. แนวให้ความรู้ / สรุปสาระ (Educational)",
            "2. แนวขายสินค้า / โปรโมชัน (Sales & Promo)",
            "3. แนวเล่าเรื่อง / แรงบันดาลใจ (Storytelling)"
        ]
    )
    st.info("💡 ภาพประกอบถูกเจนขึ้นมาใหม่ด้วย FLUX AI แบบเรียลไทม์")

# 3. พื้นที่หลัก
st.title("🚀 AI Social Content Generator")
st.caption("ระบบช่วยคิดคอนเทนต์ สร้างแคปชัน และเจนภาพประกอบอัตโนมัติ")

topic = st.text_input("📌 กรอกหัวข้อ / สินค้าที่ต้องการโพสต์:", value="กาแฟเพื่อสุขภาพ")

# ฟังก์ชันดึงภาพ AI แบบปลอดภัย (ล็อก Prompt เป็นภาษาอังกฤษบริสุทธิ์)
def get_flux_image(style):
    seed = random.randint(1, 999999)
    
    # เลือก Prompt ภาษาอังกฤษล้วนตามสไตล์ เพื่อไม่ให้ URL พัง
    if "1." in style:
        prompt = "professional modern technology infographic banner, minimalist vector graphic design, clean lighting, 8k"
    elif "2." in style:
        prompt = "commercial product photography banner, luxury composition, vibrant studio lighting, cinematic 3d render"
    else:
        prompt = "inspiring artistic background banner, golden hour atmosphere, high quality photography, masterpiece"

    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux&seed={seed}&nologo=true"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(image_url, headers=headers, timeout=15)
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content
    except Exception:
        pass
    return None

if st.button("✨ สั่ง AI สร้างโพสต์ (พร้อมรูปภาพ)", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("⚠️ กรุณากรอกหัวข้อยอดนิยมก่อนเริ่มครับ")
    else:
        status_box = st.status("🤖 AI กำลังทำงาน...", expanded=True)
        
        with status_box:
            st.write("🧠 1. กำลังสร้างแคปชันภาษาไทย...")
            time.sleep(1)
            
            # โลจิกแคปชันภาษาไทย
            if "1." in style_option:
                caption = f"💡 **[สาระน่ารู้] {topic} ที่คนยุคนี้ต้องรู้!**\n\nเคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงกลายเป็นสิ่งสำคัญในตอนนี้?\n\nวันนี้สรุป 3 หัวใจสำคัญมาให้แล้วครับ 👇\n🔹 **1. จุดเริ่มต้น:** เข้าใจง่าย นำไปใช้ได้ทันที\n🔹 **2. เครื่องมือที่ช่วยได้:** เซฟเวลาทำงานลงมากกว่า 50%\n🔹 **3. ผลลัพธ์:** เพิ่มประสิทธิภาพอย่างเห็นได้ชัด\n\nเพื่อนๆ คิดเห็นอย่างไรกับเรื่องนี้ คอมเมนต์บอกกันได้เลยครับ 👇\n\n#สาระน่ารู้ #Productivity #{topic.replace(' ', '')}"
            elif "2." in style_option:
                caption = f"🔥 **PROMOTION พิเศษ! ยกระดับ {topic} ของคุณวันนี้** 🔥\n\nคุณกำลังเจอ ปัญหาเหล่านี้อยู่ใช่ไหม? ยุ่งยาก ใช้เวลานาน และไม่ได้ผลลัพธ์ตามที่ต้องการ...\n\n✨ **ขอแนะนำโซลูชันที่จะเปลี่ยนชีวิตคุณ:**\n✅ ประหยัดเวลาขึ้น 3 เท่า\n✅ ใช้งานง่าย ไม่ซับซ้อน\n✅ คุ้มค่า ตอบโจทย์ทุกการใช้งาน\n\n🎁 **ข้อเสนอพิเศษเฉพาะสัปดาห์นี้เท่านั้น!** ทักแชตเพจ รับส่วนลดพิเศษทันที 20% 📩\n\n#โปรโมชันพิเศษ #{topic.replace(' ', '')} #คุ้มค่า"
            else:
                caption = f"🌟 **เรื่องราวเปลี่ยนชีวิต: จากจุดเริ่มต้นสู่ความสำเร็จในเรื่อง {topic}**\n\n'ถ้าไม่เริ่มวันนี้ วันข้างหน้าเราก็ยังยืนอยู่ที่เดิม'\n\nหลายคนถามเข้ามาเยอะมากเกี่ยวกับการเริ่มทำ '{topic}' ข้อคิดสำคัญที่สุดคือ:\n1. ไม่ต้องรอให้พร้อม 100% ค่อยเริ่ม\n2. ความสม่ำเสมอสำคัญกว่าความสมบูรณ์แบบ\n3. เรียนรู้จากข้อผิดพลาด แล้วปรับปรุงให้ไวขึ้น\n\nขอเป็นกำลังใจให้ทุกคนที่กำลังพัฒนาตัวเองอยู่นะครับ 💪💙\n\n#แรงบันดาลใจ #{topic.replace(' ', '')}"

            st.write("🎨 2. กำลังยิง FLUX AI เพื่อเจนรูปภาพสด...")
            img_bytes = get_flux_image(style_option)
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

        # แสดงผลลัพธ์
        st.subheader("📱 พรีวิวโพสต์บน Facebook")
        col_preview, col_tools = st.columns([1.5, 1])
        
        with col_preview:
            with st.container(border=True):
                st.markdown("**Demo Brand Official** · *เมื่อสักครู่นี้* 🌎")
                st.markdown(caption)
                if img_bytes:
                    st.image(img_bytes, caption="ภาพประกอบที่สร้างโดย FLUX AI", use_container_width=True)
                else:
                    st.error("❌ เซิร์ฟเวอร์ภาพ AI คิวแน่นชั่วคราว ลองกดสร้างใหม่อีกครั้งครับ")
        
        with col_tools:
            st.markdown("### 🛠️ เครื่องมือใช้งาน")
            st.text_area("📋 ก๊อปปี้ข้อความแคปชัน:", value=caption, height=220)
            
            if img_bytes:
                st.download_button(
                    label="📥 ดาวน์โหลดรูปภาพ AI (HD)",
                    data=img_bytes,
                    file_name=f"ai_post_{topic}.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
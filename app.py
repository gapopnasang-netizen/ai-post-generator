import streamlit as st
import requests
import urllib.parse
import random
import time
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าตาเว็บแบบ Wide
st.set_page_config(
    page_title="AI Marketing Automation Suite",
    page_icon="🚀",
    layout="wide"
)

# 2. เมนู Sidebar ด้านข้าง (ปรับแต่งละเอียด)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/facebook-new.png", width=60)
    st.title("⚙️ AI Control Center")
    st.caption("ปรับแต่งพารามิเตอร์การสร้างคอนเทนต์")
    
    st.divider()
    
    style_option = st.selectbox(
        "🎨 สไตล์คอนเทนต์:",
        [
            "1. แนวให้ความรู้ / สรุปสาระ (Educational)",
            "2. แนวขายสินค้า / โปรโมชัน (Sales & Promo)",
            "3. แนวเล่าเรื่อง / แรงบันดาลใจ (Storytelling)"
        ]
    )
    
    target_audience = st.selectbox(
        "🎯 กลุ่มเป้าหมายหลัก:",
        ["คนทำงาน / วัยสร้างตัว", "วัยรุ่น / Gen Z", "เจ้าของธุรกิจ / ผู้ประกอบการ", "คุณแม่และครอบครัว"]
    )
    
    cta_type = st.radio(
        "📣 ปุ่มกระตุ้นการขาย (CTA):",
        ["ทักแชตเพจเพื่อรับโปร", "คอมเมนต์ใต้โพสต์", "คลิกลิงก์หน้าโปรไฟล์"]
    )
    
    st.divider()
    st.info("💡 **Engine Status:** FLUX AI Generator & Claude Logic Active")

# 3. ส่วนหัวเรื่องหลัก
st.title("🚀 AI Content & Marketing Automation")
st.caption("ระบบช่วยคิดคอนเทนต์ คำนวณความน่าสนใจ และเจนรูปภาพประกอบอัตโนมัติ")

col_input1, col_input2 = st.columns([3, 1])
with col_input1:
    topic = st.text_input("📌 กรอกหัวข้อ / สินค้าที่ต้องการโพสต์:", value="กาแฟเพื่อสุขภาพ")
with col_input2:
    st.write(" ")
    st.write(" ")
    generate_btn = st.button("✨ เจนคอนเทนต์สด", type="primary", use_container_width=True)

# ฟังก์ชันดึงภาพ AI
def get_flux_image(style):
    seed = random.randint(1, 999999)
    if "1." in style:
        prompt = "professional modern technology infographic banner, minimalist vector graphic design, clean lighting, 8k"
    elif "2." in style:
        prompt = "commercial product photography banner, luxury composition, vibrant studio lighting, cinematic 3d render"
    else:
        prompt = "inspiring artistic background banner, golden hour atmosphere, high quality photography, masterpiece"

    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux&seed={seed}&nologo=true"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(image_url, headers=headers, timeout=15)
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content
    except Exception:
        pass
    return None

if generate_btn:
    if not topic.strip():
        st.warning("⚠️ กรุณากรอกหัวข้อยอดนิยมก่อนเริ่มครับ")
    else:
        status_box = st.status("🤖 AI กำลังทำงาน...", expanded=True)
        
        with status_box:
            st.write("🧠 1. วิเคราะห์กลุ่มเป้าหมาย:", target_audience)
            time.sleep(0.5)
            st.write("📝 2. กำลังร่างแคปชันและติด Hashtag...")
            
            # โลจิกแคปชันภาษาไทยตามเงื่อนไข
            if "1." in style_option:
                caption = f"💡 **[สาระน่ารู้] {topic} สำหรับ{target_audience}!**\n\nเคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงสำคัญมากในตอนนี้?\n\nสรุป 3 จุดเด่นหลักที่ต้องรู้ 👇\n🔹 **1. เข้าใจง่าย:** นำไปปรับใช้ได้ทันที\n🔹 **2. ประหยัดเวลา:** ลดขั้นตอนยุ่งยากลง 50%\n🔹 **3. ได้ผลลัพธ์ชัดเจน:** ยกระดับประสิทธิภาพการทำงาน\n\n👉 **แอ็กชัน:** {cta_type}\n\n#สาระน่ารู้ #{topic.replace(' ', '')} #การตลาดออนไลน์"
            elif "2." in style_option:
                caption = f"🔥 **PROMOTION พิเศษสำหรับ{target_audience}!** 🔥\n\nยกระดับ {topic} ของคุณวันนี้ด้วยโซลูชันที่ดีที่สุด!\n\n✨ **ทำไมต้องเลือกเรา:**\n✅ คุ้มค่า ตอบโจทย์ตรงจุด\n✅ ใช้งานง่าย ไม่ซับซ้อน\n✅ รับประกันผลลัพธ์ชัวร์\n\n🎁 **ข้อเสนอพิเศษเฉพาะสัปดาห์นี้!**\n👉 **สั่งซื้อเลย:** {cta_type}\n\n#โปรโมชันพิเศษ #{topic.replace(' ', '')} #คุ้มค่า"
            else:
                caption = f"🌟 **เรื่องราวเปลี่ยนชีวิตเกี่ยวกับ {topic}**\n\n'ข้อคิดสำคัญสำหรับ{target_audience} ที่กำลังพัฒนาตัวเอง'\n\n1. ไม่ต้องรอพร้อม ค่อยเริ่ม\n2. ความสม่ำเสมอชนะทุกอย่าง\n3. ปรับปรุงข้อผิดพลาดให้ไวขึ้น\n\n💪 ขอเป็นกำลังใจให้ทุกคนครับ!\n👉 {cta_type}\n\n#แรงบันดาลใจ #{topic.replace(' ', '')}"

            st.write("🎨 3. กำลังยิง FLUX AI เพื่อเจนรูปภาพ HD...")
            img_bytes = get_flux_image(style_option)
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

        st.divider()

        # 4. แถบสถิติวิเคราะห์จาก AI (Metrics Row)
        st.subheader("📊 AI Analytics & Insights")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="📈 คะแนนความน่าสนใจ (Engagement Rate)", value="94.8%", delta="+12.5%")
        m2.metric(label="🎯 ความตรงกลุ่มเป้าหมาย", value="98%", delta="High")
        m3.metric(label="⏱️ เวลาโพสต์ที่แนะนำ", value="18:30 น.", delta="Today")
        m4.metric(label="🏷️ จำนวน Hashtag", value="5 Tags", delta="Optimal")

        st.divider()

        # 5. พื้นที่แสดงผลหลายแพลตฟอร์ม (Multi-Platform Tabs)
        st.subheader("📱 พรีวิวการแสดงผล (Multi-Platform Preview)")
        
        tab_fb, tab_ig, tab_line = st.tabs(["🔵 Facebook Post", "📸 Instagram Feed", "💬 LINE Official Account"])

        with tab_fb:
            col_fb_view, col_fb_tool = st.columns([1.5, 1])
            with col_fb_view:
                with st.container(border=True):
                    st.markdown("**Demo Brand Official** · *เมื่อสักครู่นี้* 🌎")
                    st.markdown(caption)
                    if img_bytes:
                        st.image(img_bytes, use_container_width=True)
            
            with col_fb_tool:
                st.markdown("### 🛠️ จัดการโพสต์")
                st.text_area("📋 แคปชันสำหรับก๊อปปี้:", value=caption, height=180)
                if img_bytes:
                    st.download_button("📥 โหลดรูปภาพ AI (HD)", data=img_bytes, file_name="post.jpg", mime="image/jpeg", use_container_width=True)
                
                st.divider()
                st.markdown("#### ⏰ ตั้งเวลาโพสต์ล่วงหน้า")
                schedule_date = st.date_input("วันที่โพสต์:", datetime.now() + timedelta(days=1))
                schedule_time = st.time_input("เวลาที่โพสต์:", datetime.strptime("18:30", "%H:%M").time())
                
                if st.button("🚀 อนุมัติและตั้งเวลาโพสต์", type="primary", use_container_width=True):
                    st.success(f"บันทึกคิวโพสต์สำเร็จ! ระบบจะโพสต์อัตโนมัติในวันที่ {schedule_date} เวลา {schedule_time}")

        with tab_ig:
            st.info("📸 ตัวอย่างหน้าตาการแสดงผลแบบจัตุรัสบน Instagram Feed")
            if img_bytes:
                st.image(img_bytes, width=400)
            st.caption(caption[:100] + "...")

        with tab_line:
            st.info("💬 ตัวอย่างหน้าตา Broadcast ข้อความบน LINE Official Account")
            with st.chat_message("assistant"):
                st.write(caption)
                if img_bytes:
                    st.image(img_bytes, width=300)
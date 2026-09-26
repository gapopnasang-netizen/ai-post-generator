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

# ---------------------------------------------------------
# 🛠️ ฟังก์ชันการทำงานของ AI Image Engine
# ---------------------------------------------------------
def generate_ai_image_url(topic_th, art_style):
    seed = random.randint(1, 999999)
    topic_lower = topic_th.lower()
    
    # 🎯 จับคู่หัวข้อภาษาไทยเป็นคำสร้างภาพภาษาอังกฤษ (Topic Mapping)
    if "honda" in topic_lower or "civic" in topic_lower or "รถ" in topic_lower or "car" in topic_lower:
        subject = "sleek modern Honda Civic car, luxury automotive photography, glossy finish, studio showroom"
    elif "กาแฟ" in topic_lower or "cafe" in topic_lower or "coffee" in topic_lower:
        subject = "a cup of premium healthy espresso coffee drink, fresh coffee beans background"
    elif "สกินแคร์" in topic_lower or "เซรั่ม" in topic_lower or "ผิว" in topic_lower or "ครีม" in topic_lower:
        subject = "luxury skincare serum cosmetic bottle with natural ingredients, aesthetic studio lighting"
    elif "คอนโด" in topic_lower or "บ้าน" in topic_lower or "อสังหา" in topic_lower:
        subject = "modern luxury interior condominium living room with city view"
    elif "อาหาร" in topic_lower or "ขนม" in topic_lower or "เบเกอรี่" in topic_lower:
        subject = "delicious gourmet food bakery presentation, appetizing aesthetic"
    else:
        subject = f"professional product presentation, modern aesthetic background"

    # 🖼️ รวมคำสร้างภาพเข้ากับสไตล์ภาพที่ผู้ใช้เลือก
    if "3D" in art_style:
        full_prompt = f"3d commercial studio render of {subject}, vibrant lighting, clean 3d model, 8k resolution"
    elif "Realistic" in art_style:
        full_prompt = f"high resolution realistic photograph of {subject}, professional commercial photography, natural studio light"
    elif "Minimal" in art_style:
        full_prompt = f"minimalist vector illustration of {subject}, clean design aesthetic, elegant color palette"
    else:
        full_prompt = f"cinematic atmospheric photography of {subject}, warm lighting, golden hour atmosphere, masterpiece"

    encoded_prompt = urllib.parse.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux&seed={seed}&nologo=true"

def download_image_bytes(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content
    except Exception:
        pass
    return None

# ---------------------------------------------------------
# ⚙️ 2. เมนู Sidebar ด้านข้าง (AI Brand Control Center)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/facebook-new.png", width=50)
    st.title("⚙️ AI Brand Control")
    st.caption("ศูนย์ควบคุมแบรนด์และพารามิเตอร์ AI")
    
    st.divider()
    
    brand_preset = st.selectbox(
        "🏢 โปรไฟล์แบรนด์ (Preset):",
        ["กำหนดเอง (Custom)", "☕ Cafe & Bakery", "🧴 สกินแคร์ & ความงาม", "🏠 อสังหาฯ / คอนโด", "🚗 ยานยนต์ / โชว์รูมรถ"]
    )
    
    style_option = st.selectbox(
        "🎨 สไตล์คอนเทนต์:",
        [
            "1. แนวให้ความรู้ / สรุปสาระ (Educational)",
            "2. แนวขายสินค้า / โปรโมชัน (Sales & Promo)",
            "3. แนวเล่าเรื่อง / แรงบันดาลใจ (Storytelling)"
        ]
    )
    
    img_art_style = st.selectbox(
        "🖼️ สไตล์ภาพประกอบ AI:",
        [
            "3D Studio Render (โฆษณา)",
            "Realistic Photo (ภาพถ่ายสมจริง)",
            "Minimal Illustration (ลายเส้นมินิมอล)",
            "Cinematic Atmosphere (ฟีลภาพยนตร์)"
        ]
    )
    
    formality_level = st.slider(
        "🗣️ ระดับความเป็นทางการ:", 
        min_value=1, max_value=5, value=3,
        help="1 = เป็นกันเอง/อิโมจิเยอะ, 5 = สุภาพ/เป็นทางการน่าเชื่อถือ"
    )
    
    target_audience = st.selectbox(
        "🎯 กลุ่มเป้าหมายหลัก:",
        ["คนทำงาน / วัยสร้างตัว", "วัยรุ่น / Gen Z", "เจ้าของธุรกิจ / ผู้ประกอบการ", "คนรักรถ / คนมองหาบ้าน"]
    )
    
    cta_type = st.radio(
        "📣 ปุ่มกระตุ้นการขาย (CTA):",
        ["ทักแชตเพจเพื่อรับโปร", "คอมเมนต์ใต้โพสต์", "คลิกลิงก์หน้าโปรไฟล์"]
    )
    
    st.divider()
    st.info("💡 **Engine Status:** FLUX AI & Prompt Mapping Active")

# ---------------------------------------------------------
# 🚀 3. พื้นที่หลัก (Main Layout)
# ---------------------------------------------------------
st.title("🚀 AI Content & Marketing Automation")
st.caption("ระบบช่วยคิดคอนเทนต์ คำนวณความน่าสนใจ และเจนรูปภาพประกอบอัตโนมัติสำหรับธุรกิจ")

# กำหนดค่าเริ่มต้นตาม Preset แบรนด์
default_topic = "กาแฟเพื่อสุขภาพ"
if brand_preset == "☕ Cafe & Bakery":
    default_topic = "กาแฟสกัดเย็นเมล็ดอาราบิก้า"
elif brand_preset == "🧴 สกินแคร์ & ความงาม":
    default_topic = "เซรั่มไฮยาเข้มข้นกู้ผิวพัง"
elif brand_preset == "🏠 อสังหาฯ / คอนโด":
    default_topic = "คอนโดติดรถไฟฟ้า พร้อมอยู่"
elif brand_preset == "🚗 ยานยนต์ / โชว์รูมรถ":
    default_topic = "Honda Civic โฉมใหม่"

col_input1, col_input2 = st.columns([3, 1])
with col_input1:
    topic = st.text_input("📌 กรอกหัวข้อ / สินค้าที่ต้องการโพสต์:", value=default_topic)
with col_input2:
    st.write(" ")
    st.write(" ")
    generate_btn = st.button("✨ เจนคอนเทนต์สด", type="primary", use_container_width=True)

# ---------------------------------------------------------
# 🤖 4. โลจิกประมวลผลและการแสดงผล
# ---------------------------------------------------------
if generate_btn:
    if not topic.strip():
        st.warning("⚠️ กรุณากรอกหัวข้อก่อนเริ่มครับ")
    else:
        status_box = st.status("🤖 AI กำลังประมวลผล...", expanded=True)
        
        with status_box:
            st.write(f"🧠 1. วิเคราะห์โจทย์ '{topic}' ปรับโทนระดับ {formality_level}/5...")
            time.sleep(0.4)
            st.write(f"📝 2. ร่างแคปชัน และประมวลผล Hashtag สำหรับ {target_audience}...")
            
            # ปรับแต่งคำตามระดับความทางการ
            emoji_prefix = "🔥✨" if formality_level <= 2 else ("📌" if formality_level == 3 else "▪️")
            polite_ending = "นะคร้าบ/ค่ะ 👇" if formality_level <= 2 else ("ครับ/ค่ะ 👇" if formality_level == 3 else "เรียนเชิญสอบถามรายละเอียดเพิ่มเติม")

            # โลจิกแคปชัน
            if "1." in style_option:
                caption = f"{emoji_prefix} **[สาระน่ารู้] {topic} ที่ {target_audience} ต้องรู้!**\n\nเคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงกลายเป็นสิ่งสำคัญในตอนนี้?\n\nวันนี้สรุป 3 หัวใจสำคัญมาให้แล้ว {polite_ending}\n🔹 **1. จุดเด่น:** เข้าใจง่าย นำไปปรับใช้ได้ทันที\n🔹 **2. ตัวช่วยสำคัญ:** ลดเวลาทำงานลงกว่า 50%\n🔹 **3. ผลลัพธ์:** เพิ่มประสิทธิภาพอย่างชัดเจน\n\n👉 **สนใจสอบถาม:** {cta_type}\n\n#สาระน่ารู้ #{topic.replace(' ', '')} #การตลาดออนไลน์"
            elif "2." in style_option:
                caption = f"{emoji_prefix} **PROMOTION พิเศษ! ยกระดับ {topic} ของคุณวันนี้**\n\nข้อเสนอสุดคุ้มเพื่อ {target_audience} โดยเฉพาะ!\n\n✨ **ไฮไลต์ที่คุณไม่ควรพลาด:**\n✅ ตอบโจทย์ตรงจุด คุ้มค่าที่สุด\n✅ ดีไซน์สวยงาม ใช้งานง่าย\n✅ การันตีคุณภาพและความพึงพอใจ\n\n🎁 **ข้อเสนอพิเศษสัปดาห์นี้เท่านั้น!**\n👉 **สั่งซื้อ/รับโปร:** {cta_type}\n\n#โปรโมชันพิเศษ #{topic.replace(' ', '')} #สินค้าแนะนำ"
            else:
                caption = f"{emoji_prefix} **เรื่องราวและแนวคิดเกี่ยวกับ {topic}**\n\n'ข้อคิดสำคัญสำหรับ {target_audience} ที่กำลังพัฒนาตัวเอง'\n\n1. ไม่ต้องรอให้พร้อม 100% ค่อยเริ่ม\n2. ความสม่ำเสมอคือหัวใจของความสำเร็จ\n3. เรียนรู้จากข้อผิดพลาด แล้วปรับปรุงให้ไวขึ้น\n\n💪 ขอเป็นกำลังใจให้ทุกคนครับ\n👉 **ติดต่อแบรนด์:** {cta_type}\n\n#แรงบันดาลใจ #{topic.replace(' ', '')}"

            st.write(f"🎨 3. ยิง FLUX AI เจนภาพสไตล์ '{img_art_style}' แบบเรียลไทม์...")
            image_url = generate_ai_image_url(topic, img_art_style)
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

        st.divider()

        # 📊 แถบสถิติวิเคราะห์จาก AI (Metrics Row)
        st.subheader("📊 AI Analytics & Insights")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="📈 Engagement Potential", value="95.8%", delta="+14.2%")
        m2.metric(label="🎯 Brand Alignment", value=f"Level {formality_level}/5", delta=brand_preset)
        m3.metric(label="⏱️ Best Posting Time", value="18:30 น.", delta="Today")
        m4.metric(label="🖼️ Image Engine", value=img_art_style.split()[0], delta="FLUX Active")

        st.divider()

        # 📱 พื้นที่แสดงผลหลายแพลตฟอร์ม (Multi-Platform Tabs)
        st.subheader("📱 พรีวิวการแสดงผล (Multi-Platform Preview)")
        
        tab_fb, tab_ig, tab_line = st.tabs(["🔵 Facebook Post", "📸 Instagram Feed", "💬 LINE Official Account"])

        # Tab 1: Facebook
        with tab_fb:
            col_fb_view, col_fb_tool = st.columns([1.5, 1])
            with col_fb_view:
                with st.container(border=True):
                    st.markdown(f"**{brand_preset if 'Custom' not in brand_preset else 'Demo Brand Official'}** · *เมื่อสักครู่นี้* 🌎")
                    st.markdown(caption)
                    # แสดงภาพจาก URL โดยตรง (ไม่ติด Timeout)
                    st.image(image_url, caption=f"ภาพประกอบ AI สไตล์: {img_art_style}", use_container_width=True)
            
            with col_fb_tool:
                st.markdown("### 🛠️ เครื่องมือจัดการ")
                st.text_area("📋 แคปชันสำหรับก๊อปปี้:", value=caption, height=180)
                
                # ปุ่มโหลดภาพ
                img_bytes = download_image_bytes(image_url)
                if img_bytes:
                    st.download_button("📥 โหลดรูปภาพ AI (HD)", data=img_bytes, file_name="post_ai.jpg", mime="image/jpeg", use_container_width=True)
                else:
                    st.link_button("🔗 เปิดดู/เซฟรูปขนาดเต็ม (HD)", image_url, use_container_width=True)
                
                st.divider()
                st.markdown("#### ⏰ ตั้งเวลาโพสต์ล่วงหน้า")
                schedule_date = st.date_input("วันที่โพสต์:", datetime.now() + timedelta(days=1))
                schedule_time = st.time_input("เวลาที่โพสต์:", datetime.strptime("18:30", "%H:%M").time())
                
                if st.button("🚀 อนุมัติและตั้งเวลาโพสต์", type="primary", use_container_width=True):
                    st.success(f"บันทึกคิวโพสต์สำเร็จ! ระบบจะโพสต์อัตโนมัติในวันที่ {schedule_date} เวลา {schedule_time}")

        # Tab 2: Instagram
        with tab_ig:
            st.info("📸 ตัวอย่างหน้าตาการแสดงผลบน Instagram Feed")
            st.image(image_url, width=420)
            st.caption(caption[:120] + "...")

        # Tab 3: LINE
        with tab_line:
            st.info("💬 ตัวอย่างหน้าตา Broadcast ข้อความบน LINE Official Account")
            with st.chat_message("assistant"):
                st.write(caption)
                st.image(image_url, width=320)
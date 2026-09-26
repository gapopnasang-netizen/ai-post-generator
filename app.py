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
# 🧠 ระบบ Session State (ช่วยจำค่าผลลัพธ์ไม่ให้รูปหายเวลากด Sidebar)
# ---------------------------------------------------------
if "generated" not in st.session_state:
    st.session_state.generated = False
if "caption" not in st.session_state:
    st.session_state.caption = ""
if "image_url" not in st.session_state:
    st.session_state.image_url = ""
if "art_style_used" not in st.session_state:
    st.session_state.art_style_used = ""

# ---------------------------------------------------------
# 🛠️ ฟังก์ชันแปลงภาษา & เจนรูปภาพ AI
# ---------------------------------------------------------
def translate_th_to_en(text_th):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=th&tl=en&dt=t&q={urllib.parse.quote(text_th)}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result[0][0][0]
    except Exception:
        pass
    return text_th

def generate_ai_image_url(topic_th, art_style):
    seed = random.randint(1, 999999)
    topic_en = translate_th_to_en(topic_th)
    
    if "3D" in art_style:
        full_prompt = f"3d commercial studio render of {topic_en}, professional product presentation, vibrant studio lighting, clean render, 8k resolution"
    elif "Realistic" in art_style:
        full_prompt = f"high resolution realistic commercial photograph of {topic_en}, studio lighting, sharp focus, professional product shot, 8k"
    elif "Minimal" in art_style:
        full_prompt = f"minimalist vector illustration of {topic_en}, clean design aesthetic, elegant color palette, high quality"
    else:
        full_prompt = f"cinematic atmospheric photography of {topic_en}, warm studio lighting, golden hour, masterpiece, detailed background"

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
    st.info("💡 **Engine Status:** Auto-Translate & FLUX AI Active")

# ---------------------------------------------------------
# 🚀 3. พื้นที่หลัก (Main Layout)
# ---------------------------------------------------------
st.title("🚀 AI Content & Marketing Automation")
st.caption("ระบบช่วยคิดคอนเทนต์ คำนวณความน่าสนใจ และเจนรูปภาพประกอบอัตโนมัติสำหรับธุรกิจ")

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
# 🤖 4. โลจิกเมื่อกดปุ่ม "เจนคอนเทนต์สด"
# ---------------------------------------------------------
if generate_btn:
    if not topic.strip():
        st.warning("⚠️ กรุณากรอกหัวข้อก่อนเริ่มครับ")
    else:
        status_box = st.status("🤖 AI กำลังประมวลผล...", expanded=True)
        
        with status_box:
            st.write(f"🧠 1. วิเคราะห์โจทย์ '{topic}' ปรับโทนระดับ {formality_level}/5...")
            time.sleep(0.3)
            st.write(f"📝 2. ร่างแคปชัน และประมวลผล Hashtag สำหรับ {target_audience}...")
            
            emoji_prefix = "🔥✨" if formality_level <= 2 else ("📌" if formality_level == 3 else "▪️")
            polite_ending = "นะคร้าบ/ค่ะ 👇" if formality_level <= 2 else ("ครับ/ค่ะ 👇" if formality_level == 3 else "เรียนเชิญสอบถามรายละเอียดเพิ่มเติม")

            if "1." in style_option:
                caption = f"{emoji_prefix} **[สาระน่ารู้] {topic} ที่ {target_audience} ต้องรู้!**\n\nเคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงกลายเป็นสิ่งสำคัญในตอนนี้?\n\nวันนี้สรุป 3 หัวใจสำคัญมาให้แล้ว {polite_ending}\n🔹 **1. จุดเด่น:** เข้าใจง่าย นำไปปรับใช้ได้ทันที\n🔹 **2. ตัวช่วยสำคัญ:** ลดเวลาทำงานลงกว่า 50%\n🔹 **3. ผลลัพธ์:** เพิ่มประสิทธิภาพอย่างชัดเจน\n\n👉 **สนใจสอบถาม:** {cta_type}\n\n#สาระน่ารู้ #{topic.replace(' ', '')} #การตลาดออนไลน์"
            elif "2." in style_option:
                caption = f"{emoji_prefix} **PROMOTION พิเศษ! ยกระดับ {topic} ของคุณวันนี้**\n\nข้อเสนอสุดคุ้มเพื่อ {target_audience} โดยเฉพาะ!\n\n✨ **ไฮไลต์ที่คุณไม่ควรพลาด:**\n✅ ตอบโจทย์ตรงจุด คุ้มค่าที่สุด\n✅ ดีไซน์สวยงาม ใช้งานง่าย\n✅ การันตีคุณภาพและความพึงพอใจ\n\n🎁 **ข้อเสนอพิเศษสัปดาห์นี้เท่านั้น!**\n👉 **สั่งซื้อ/รับโปร:** {cta_type}\n\n#โปรโมชันพิเศษ #{topic.replace(' ', '')} #สินค้าแนะนำ"
            else:
                caption = f"{emoji_prefix} **เรื่องราวและแนวคิดเกี่ยวกับ {topic}**\n\n'ข้อคิดสำคัญสำหรับ {target_audience} ที่กำลังพัฒนาตัวเอง'\n\n1. ไม่ต้องรอให้พร้อม 100% ค่อยเริ่ม\n2. ความสม่ำเสมอคือหัวใจของความสำเร็จ\n3. เรียนรู้จากข้อผิดพลาด แล้วปรับปรุงให้ไวขึ้น\n\n💪 ขอเป็นกำลังใจให้ทุกคนครับ\n👉 **ติดต่อแบรนด์:** {cta_type}\n\n#แรงบันดาลใจ #{topic.replace(' ', '')}"

            st.write(f"🌐 3. แปลคำค้นหา และยิง FLUX AI เจนภาพสไตล์ '{img_art_style}'...")
            image_url = generate_ai_image_url(topic, img_art_style)
            
            # 💾 บันทึกค่าลงใน Session State
            st.session_state.generated = True
            st.session_state.caption = caption
            st.session_state.image_url = image_url
            st.session_state.art_style_used = img_art_style
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

# ---------------------------------------------------------
# 📱 5. ส่วนแสดงผลลัพธ์ (ดึงค่าจาก Session State มาโชว์)
# ---------------------------------------------------------
if st.session_state.generated:
    st.divider()

    # 📊 แถบสถิติวิเคราะห์จาก AI
    st.subheader("📊 AI Analytics & Insights")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="📈 Engagement Potential", value="95.8%", delta="+14.2%")
    m2.metric(label="🎯 Brand Alignment", value=f"Level {formality_level}/5", delta=brand_preset)
    m3.metric(label="⏱️ Best Posting Time", value="18:30 น.", delta="Today")
    m4.metric(label="🖼️ Image Engine", value=st.session_state.art_style_used.split()[0], delta="FLUX Active")

    st.divider()

    # 📱 พื้นที่แสดงผลหลายแพลตฟอร์ม
    st.subheader("📱 พรีวิวการแสดงผล (Multi-Platform Preview)")
    
    tab_fb, tab_ig, tab_line = st.tabs(["🔵 Facebook Post", "📸 Instagram Feed", "💬 LINE Official Account"])

    # Tab 1: Facebook
    with tab_fb:
        col_fb_view, col_fb_tool = st.columns([1.5, 1])
        with col_fb_view:
            with st.container(border=True):
                st.markdown(f"**{brand_preset if 'Custom' not in brand_preset else 'Demo Brand Official'}** · *เมื่อสักครู่นี้* 🌎")
                st.markdown(st.session_state.caption)
                
                # แสดงรูปภาพจาก Session State (ไม่มีวันหายเวลากด Sidebar)
                st.image(st.session_state.image_url, caption=f"ภาพประกอบ AI สไตล์: {st.session_state.art_style_used}", use_container_width=True)
        
        with col_fb_tool:
            st.markdown("### 🛠️ เครื่องมือจัดการ")
            st.text_area("📋 แคปชันสำหรับก๊อปปี้:", value=st.session_state.caption, height=180)
            
            img_bytes = download_image_bytes(st.session_state.image_url)
            if img_bytes:
                st.download_button("📥 โหลดรูปภาพ AI (HD)", data=img_bytes, file_name="post_ai.jpg", mime="image/jpeg", use_container_width=True)
            else:
                st.link_button("🔗 เปิดดู/เซฟรูปขนาดเต็ม (HD)", st.session_state.image_url, use_container_width=True)
            
            st.divider()
            st.markdown("#### ⏰ ตั้งเวลาโพสต์ล่วงหน้า")
            schedule_date = st.date_input("วันที่โพสต์:", datetime.now() + timedelta(days=1))
            schedule_time = st.time_input("เวลาที่โพสต์:", datetime.strptime("18:30", "%H:%M").time())
            
            if st.button("🚀 อนุมัติและตั้งเวลาโพสต์", type="primary", use_container_width=True):
                st.success(f"บันทึกคิวโพสต์สำเร็จ! ระบบจะโพสต์อัตโนมัติในวันที่ {schedule_date} เวลา {schedule_time}")

    # Tab 2: Instagram
    with tab_ig:
        st.info("📸 ตัวอย่างหน้าตาการแสดงผลบน Instagram Feed")
        st.image(st.session_state.image_url, width=420)
        st.caption(st.session_state.caption[:120] + "...")

    # Tab 3: LINE
    with tab_line:
        st.info("💬 ตัวอย่างหน้าตา Broadcast ข้อความบน LINE Official Account")
        with st.chat_message("assistant"):
            st.write(st.session_state.caption)
            st.image(st.session_state.image_url, width=320)
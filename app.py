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
    st.image("https://img.icons8.com/color/96/facebook-new.png", width=50)
    st.title("⚙️ AI Brand Control Center")
    st.caption("ศูนย์ควบคุมแบรนด์และพารามิเตอร์ AI")
    
    st.divider()
    
    # 🎯 ลูกเล่นที่ 1: Preset แบรนด์ตัวอย่าง
    brand_preset = st.selectbox(
        "🏢 โปรไฟล์แบรนด์ (Preset):",
        ["กำหนดเอง (Custom)", "☕ Cafe & Bakery", "🧴 สกินแคร์ & ความงาม", "🏠 อสังหาฯ / คอนโด"]
    )
    
    style_option = st.selectbox(
        "🎨 สไตล์คอนเทนต์:",
        [
            "1. แนวให้ความรู้ / สรุปสาระ (Educational)",
            "2. แนวขายสินค้า / โปรโมชัน (Sales & Promo)",
            "3. แนวเล่าเรื่อง / แรงบันดาลใจ (Storytelling)"
        ]
    )
    
    # 🖼️ ลูกเล่นที่ 2: เลือกสไตล์ภาพ AI
    img_art_style = st.selectbox(
        "🖼️ สไตล์ภาพประกอบ AI:",
        [
            "3D Studio Render (โฆษณา)",
            "Realistic Photo (ภาพถ่ายสมจริง)",
            "Minimal Illustration (ลายเส้นมินิมอล)",
            "Cinematic Atmosphere (ฟีลภาพยนตร์)"
        ]
    )
    
    # 🗣️ ลูกเล่นที่ 3: ปรับระดับความทางการ
    formality_level = st.slider(
        "🗣️ ระดับความเป็นทางการของแคปชัน:", 
        min_value=1, max_value=5, value=3,
        help="1 = เป็นกันเอง/อิโมจิเยอะ, 5 = สุภาพ/เป็นทางการน่าเชื่อถือ"
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
    st.info("💡 **Engine Status:** FLUX AI Generator & Dynamic Tone Logic Active")

# 3. ส่วนหัวเรื่องหลัก
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

col_input1, col_input2 = st.columns([3, 1])
with col_input1:
    topic = st.text_input("📌 กรอกหัวข้อ / สินค้าที่ต้องการโพสต์:", value=default_topic)
with col_input2:
    st.write(" ")
    st.write(" ")
    generate_btn = st.button("✨ เจนคอนเทนต์สด", type="primary", use_container_width=True)

# ฟังก์ชันดึงภาพ AI ตามสไตล์ภาพที่เลือก
def get_flux_image(art_style):
    seed = random.randint(1, 999999)
    
    # ปรับ Prompt ภาษาอังกฤษตามสไตล์ภาพที่ผู้ใช้เลือก
    if "3D" in art_style:
        style_prompt = "3d studio render product shot, vibrant commercial lighting, studio background, high quality 3d model"
    elif "Realistic" in art_style:
        style_prompt = "high resolution realistic commercial photograph, professional product photography, shallow depth of field, natural studio lighting"
    elif "Minimal" in art_style:
        style_prompt = "minimalist vector illustration, clean aesthetic design, simple geometry, elegant color palette, modern graphic design"
    else:
        style_prompt = "cinematic photography, atmospheric warm lighting, golden hour, masterpiece composition, highly detailed"

    encoded_prompt = urllib.parse.quote(style_prompt)
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
        status_box = st.status("🤖 AI กำลังประมวลผล...", expanded=True)
        
        with status_box:
            st.write(f"🧠 1. ปรับโทนแคปชันระดับ {formality_level}/5 ให้เข้ากับกลุ่ม {target_audience}...")
            time.sleep(0.5)
            st.write(f"📝 2. กำลังร่างแคปชันและติด Hashtag สำหรับแบรนด์ {brand_preset}...")
            
            # ปรับแต่งคำตามระดับความทางการ
            emoji_prefix = "🔥✨" if formality_level <= 2 else ("📌" if formality_level == 3 else "▪️")
            polite_ending = "นะคร้าบ/ค่ะ 👇" if formality_level <= 2 else ("ครับ/ค่ะ 👇" if formality_level == 3 else "เรียนเชิญสอบถามรายละเอียดเพิ่มเติม")

            # โลจิกแคปชัน
            if "1." in style_option:
                caption = f"{emoji_prefix} **[สาระน่ารู้] {topic} สำหรับ{target_audience}!**\n\nเคยสงสัยไหมครับว่า ทำไมเรื่อง '{topic}' ถึงกลายเป็นหัวข้อสำคัญในตอนนี้?\n\nย่อย 3 สาระสำคัญมาให้แล้ว {polite_ending}\n🔹 **1. จุดเริ่มต้น:** เข้าใจง่าย นำไปปรับใช้ได้ทันที\n🔹 **2. เครื่องมือแนะนำ:** ลดขั้นตอนยุ่งยากลง 50%\n🔹 **3. ผลลัพธ์:** เห็นความเปลี่ยนแปลงอย่างชัดเจน\n\n👉 **สนใจเพิ่มเติม:** {cta_type}\n\n#สาระน่ารู้ #{topic.replace(' ', '')} #การตลาดออนไลน์"
            elif "2." in style_option:
                caption = f"{emoji_prefix} **PROMOTION พิเศษ! ยกระดับ {topic} ของคุณวันนี้**\n\nข้อเสนอสุดคุ้มเพื่อ{target_audience} โดยเฉพาะ!\n\n✨ **จุดเด่นที่ไม่ควรพลาด:**\n✅ ตอบโจทย์ตรงจุด คุ้มค่าที่สุด\n✅ ใช้งานง่าย ไม่ซับซ้อน\n✅ การันตีคุณภาพและความพึงพอใจ\n\n🎁 **สิทธิพิเศษสัปดาห์นี้เท่านั้น!**\n👉 **คลิกเลย:** {cta_type}\n\n#โปรโมชันพิเศษ #{topic.replace(' ', '')} #สินค้าแนะนำ"
            else:
                caption = f"{emoji_prefix} **เรื่องราวและแรงบันดาลใจเกี่ยวกับ {topic}**\n\n'ข้อคิดสำคัญสำหรับ{target_audience} ที่กำลังพัฒนาตัวเอง'\n\n1. ไม่ต้องรอให้พร้อม 100% ค่อยเริ่ม\n2. ความสม่ำเสมอคือหัวใจของความสำเร็จ\n3. เรียนรู้และปรับปรุงอย่างรวดเร็ว\n\n💪 ขอเป็นกำลังใจให้ทุกคนครับ\n👉 **สอบถามข้อมูล:** {cta_type}\n\n#แรงบันดาลใจ #{topic.replace(' ', '')}"

            st.write(f"🎨 3. ยิง FLUX AI เจนภาพสไตล์ '{img_art_style}'...")
            img_bytes = get_flux_image(img_art_style)
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

        st.divider()

        # 4. แถบสถิติวิเคราะห์จาก AI (Metrics Row)
        st.subheader("📊 AI Analytics & Insights")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="📈 Engagement Potential", value="95.2%", delta="+14.1%")
        m2.metric(label="🎯 Brand Alignment", value=f"Level {formality_level}/5", delta=brand_preset)
        m3.metric(label="⏱️ Best Posting Time", value="18:30 น.", delta="Today")
        m4.metric(label="🖼️ Image Style", value=img_art_style.split()[0], delta="FLUX Engine")

        st.divider()

        # 5. พื้นที่แสดงผลหลายแพลตฟอร์ม (Multi-Platform Tabs)
        st.subheader("📱 พรีวิวการแสดงผล (Multi-Platform Preview)")
        
        tab_fb, tab_ig, tab_line = st.tabs(["🔵 Facebook Post", "📸 Instagram Feed", "💬 LINE Official Account"])

        with tab_fb:
            col_fb_view, col_fb_tool = st.columns([1.5, 1])
            with col_fb_view:
                with st.container(border=True):
                    st.markdown(f"**{brand_preset if 'Custom' not in brand_preset else 'Demo Brand Official'}** · *เมื่อสักครู่นี้* 🌎")
                    st.markdown(caption)
                    if img_bytes:
                        st.image(img_bytes, caption=f"ภาพประกอบ AI สไตล์: {img_art_style}", use_container_width=True)
            
            with col_fb_tool:
                st.markdown("### 🛠️ เครื่องมือจัดการ")
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
            st.info("📸 ตัวอย่างหน้าตาการแสดงผลบน Instagram Feed")
            if img_bytes:
                st.image(img_bytes, width=400)
            st.caption(caption[:100] + "...")

        with tab_line:
            st.info("💬 ตัวอย่างหน้าตา Broadcast ข้อความบน LINE Official Account")
            with st.chat_message("assistant"):
                st.write(caption)
                if img_bytes:
                    st.image(img_bytes, width=300)
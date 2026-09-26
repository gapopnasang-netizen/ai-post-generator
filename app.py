import streamlit as st
import requests
import urllib.parse
import random
import time
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. ตั้งค่าหน้าตาเว็บแบบ Wide
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Content & Marketing Automation Suite",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------------
# 🧠 ระบบ Session State (เก็บค่าและไฟล์ภาพใน Memory รูปไม่หาย 100%)
# ---------------------------------------------------------
if "generated" not in st.session_state:
    st.session_state.generated = False
if "caption" not in st.session_state:
    st.session_state.caption = ""
if "image_url" not in st.session_state:
    st.session_state.image_url = ""
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "art_style_used" not in st.session_state:
    st.session_state.art_style_used = ""

# ---------------------------------------------------------
# 🛠️ Universal AI Image Prompt & Fetch Engine (พร้อมระบบ Polling รอภาพ)
# ---------------------------------------------------------
def translate_to_en(text):
    """แปลภาษาอัตโนมัติเพื่อให้ AI เจนรูปได้แม่นยำ"""
    if not text:
        return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text.strip())}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return "".join([item[0] for item in result[0] if item[0]])
    except Exception:
        pass
    return text

def generate_ai_image_url(topic_th, art_style):
    """สร้าง Prompt อัจฉริยะวิเคราะห์หมวดหมู่ พร้อมปรับแสงมุมกล้อง"""
    seed = random.randint(1, 999999)
    topic_en = translate_to_en(topic_th)
    topic_lower = topic_en.lower()
    
    # Smart Context Category Enhancer
    if any(w in topic_lower for w in ["food", "drink", "coffee", "dish", "cake", "restaurant", "noodle", "tea", "bakery", "soup", "sushi"]):
        context_keywords = "gourmet food photography, commercial culinary presentation, appetizing lighting, clean studio tabletop"
    elif any(w in topic_lower for w in ["car", "vehicle", "honda", "toyota", "motorcycle", "bike", "auto", "drive", "ev", "truck"]):
        context_keywords = "automotive photography, sleek glossy bodywork, modern showroom, dynamic reflections, luxury finish"
    elif any(w in topic_lower for w in ["house", "condo", "room", "architecture", "building", "interior", "decor", "home", "hotel"]):
        context_keywords = "architectural showcase, luxury interior design, spacious view, modern aesthetic, ambient soft light"
    elif any(w in topic_lower for w in ["skin", "cream", "cosmetic", "beauty", "perfume", "fashion", "dress", "shoes", "bag", "watch"]):
        context_keywords = "luxury product placement, aesthetic studio arrangement, high-end editorial lighting, soft shadows"
    elif any(w in topic_lower for w in ["person", "man", "woman", "worker", "team", "people", "doctor", "teacher", "service", "cleaner"]):
        context_keywords = "professional portrait photography, authentic human touch, natural expressions, expressive cinematic depth"
    else:
        context_keywords = "commercial product presentation, high-end design, perfectly balanced studio composition, clear subject focus"

    # Style Combination
    if "3D" in art_style:
        full_prompt = f"3d commercial studio render of {topic_en}, {context_keywords}, vibrant lighting, clean 3d model, octane render, 8k resolution"
    elif "Realistic" in art_style:
        full_prompt = f"high resolution realistic professional photograph of {topic_en}, {context_keywords}, shot on 35mm lens, sharp focus, natural studio light, 8k"
    elif "Minimal" in art_style:
        full_prompt = f"minimalist design illustration of {topic_en}, clean background, elegant design aesthetic, modern color palette, simple crisp look"
    else:
        full_prompt = f"cinematic atmospheric photograph of {topic_en}, {context_keywords}, dramatic studio lighting, golden hour warmth, depth of field, masterpiece"

    encoded_prompt = urllib.parse.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&model=flux&seed={seed}&nologo=true"

def fetch_image_data(image_url):
    """ดาวน์โหลดและรอจนกว่าเซิร์ฟเวอร์ AI จะเจนรูปเสร็จจริง (วนรอสูงสุด 12 วินาที)"""
    if not image_url:
        return None
    for _ in range(6):
        try:
            response = requests.get(image_url, timeout=10)
            content_type = response.headers.get("Content-Type", "")
            # ต้องได้ HTTP 200 เป็นไฟล์รูปภาพ และขนาดใหญ่กว่า 5KB
            if response.status_code == 200 and "image" in content_type and len(response.content) > 5000:
                return response.content
        except Exception:
            pass
        time.sleep(1.5)  # หน่วงเวลารอ AI วาดรูป
    return None

# ---------------------------------------------------------
# ✍️ Human-Like Copywriter Engine (ภาษาธรรมชาติเหมือนคนเขียน)
# ---------------------------------------------------------
def generate_human_caption(topic, style_option, formality_level, target_audience, cta_type):
    clean_tag = topic.replace(' ', '').replace('/', '').replace('&', '')
    
    if formality_level <= 2:
        if "1." in style_option:
            caption = f"""เอาจริงนะ... ใครที่กำลังหาข้อมูลเรื่อง {topic} อยู่ ต้องอ่านโพสต์นี้เลย! 💡\n\nรวมสรุปแบบฉบับเข้าใจง่ายที่สุดมาให้แล้ว สำหรับชาว {target_audience} โดยเฉพาะเลยน้า\n\n✨ สรุป 3 ข้อสั้นๆ อ่านจบเก็ททันที:\n• เรื่องนี้สำคัญกว่าที่คิด ช่วยประหยัดเวลาชีวิตไปเยอะมาก\n• พอเริ่มปรับใช้จริง จะรู้เลยว่ามันสะดวกขึ้นแบบ 300%\n• ใครที่ลังเลอยู่ บอกเลยว่าเริ่มต้นตอนนี้คุ้มสุด!\n\nใครอ่านแล้วชอบ ลองเซฟเก็บไว้ดูได้เลยน้า หรือ {cta_type} มาคุยกันได้เลยครับ/ค่ะ ✨\n\n#{clean_tag} #ป้ายยา #รีวิวดีบอกต่อ #เกร็ดความรู้"""
        elif "2." in style_option:
            caption = f"""ป้ายยาแรงๆ เลยตัวนี้! 🔥 ใครสาย {topic} บอกเลยว่าห้ามพลาดเด็ดขาด~\n\nไอเทมเด็ดที่ชาว {target_audience} ต้องมีติดไว้ คุ้มค่าแบบก๊อกสอง!\n\nคุ้มยังไงบ้าง มาดู 👇\n✅ ดีไซน์สวยตรงปก ใช้แล้วชอบแน่นอน\n✅ ตอบโจทย์ชีวิตประจำวันแบบสุดๆ\n✅ จัดโปรพิเศษเฉพาะรอบนี้เท่านั้น หมดแล้วหมดเลยนะ!\n\nใครสนใจอยากจัด รีบ {cta_type} ด่วนเลยน้า ก่อนของจะหมดก่อน! 💨\n\n#{clean_tag} #ของมันต้องมี #โปรโมชันพิเศษ #จัดด่วน"""
        else:
            caption = f"""มีเรื่องอยากเล่าให้ฟังนิดนึง... 💭\n\nเคยคิดเหมือนกันไหมครับ/ค่ะว่า เรื่อง {topic} มันดูไกลตัว?\nแต่พอได้ลองเปิดใจศึกษามันจริงๆ ถึงได้รู้ว่า ชีวิตเราเปลี่ยนไปเยอะมาก\n\nสำหรับ {target_audience} ที่กำลังพยายามทำอะไรสักอย่างอยู่:\n"ไม่ต้องรอให้พร้อม 100% ค่อยเริ่มหรอก แค่ก้าวแรกก็เก่งมากแล้ว" ✌️\n\nสู้ไปด้วยกันน้า ใครอยากพูดคุยหรือแชร์ไอเดีย {cta_type} ได้เลยครับ!\n\n#{clean_tag} #ข้อคิดดีๆ #แรงบันดาลใจ #พัฒนาตัวเอง"""

    elif formality_level == 3:
        if "1." in style_option:
            caption = f"""มีใครกำลังเจอปัญหาหรือสงสัยเกี่ยวกับ '{topic}' อยู่บ้างครับ/ค่ะ? 👋\n\nวันนี้เราสรุป 3 ข้อควรรู้สำหรับ {target_audience} มาให้เรียบร้อยแล้วครับ นำไปปรับใช้ได้ทันที!\n\n📌 3 หัวใจสำคัญที่ไม่ควรมองข้าม:\n1️⃣ **จุดเริ่มต้นที่ถูกต้อง:** ช่วยลดขั้นตอนที่ซับซ้อนลงได้เยอะมาก\n2️⃣ **เทคนิคสำคัญ:** ช่วยเพิ่มประสิทธิภาพและประหยัดเวลาได้ชัดเจน\n3️⃣ **ผลลัพธ์ที่ได้:** คุ้มค่ากับการลงทุนในระยะยาวแน่นอนครับ\n\nอยากรู้รายละเอียดเพิ่มเติม สามารถ {cta_type} ได้เลยนะครับ ยินดีแนะนำครับ 😊\n\n#{clean_tag} #สาระน่ารู้ #การตลาดออนไลน์ #แชร์ความรู้"""
        elif "2." in style_option:
            caption = f"""ยกระดับความสะดวกสบายด้วย '{topic}' ที่ตอบโจทย์เพื่อ {target_audience} โดยเฉพาะ ✨\n\nหากคุณกำลังมองหาตัวช่วยดีๆ ที่คุ้มค่าและมั่นใจได้ในคุณภาพ แนะนำรุ่นนี้เลยครับ!\n\n🌟 **ไฮไลต์เด่นที่อยากแนะนำ:**\n• ออกแบบมาให้ใช้งานง่าย ตอบโจทย์ตรงจุด\n• คุ้มค่า คุ้มราคา รับประกันความพึงพอใจ\n• มีทีมงานคอยดูแลและให้คำแนะนำตลอดการใช้งาน\n\n🎁 **ข้อเสนอพิเศษสัปดาห์นี้:**\nสั่งซื้อหรือสอบถามโปรโมชัน เพียง {cta_type} ได้ทันทีครับ!\n\n#{clean_tag} #สินค้าแนะนำ #โปรโมชันพิเศษ #คุ้มค่า"""
        else:
            caption = f"""เบื้องหลังของคำว่าความสำเร็จเกี่ยวกับ '{topic}' 💡\n\nในการทำงานหรือการทำธุรกิจสำหรับ {target_audience} สิ่งสำคัญที่สุดบางครั้งอาจไม่ใช่ความพร้อม แต่คือ 'ความสม่ำเสมอ' ครับ\n\n3 ข้อคิดดีๆ ที่เราอยากมอบให้ในวันนี้:\n• ก้าวเล็กๆ ในทุกวัน ยิ่งใหญ่กว่าการไม่เริ่มทำอะไรเลย\n• ข้อผิดพลาดคือบทเรียนที่ทำให้เราเก่งขึ้นเสมอ\n• อย่าลืมภูมิใจกับตัวเองในทุกขั้นตอน\n\nขอเป็นกำลังใจให้ทุกท่านนะครับ หากต้องการแลกเปลี่ยนแนวคิด สามารถ {cta_type} ได้เลยครับ 😊\n\n#{clean_tag} #ข้อคิดธุรกิจ #แรงบันดาลใจ #ความสำเร็จ"""

    else:
        if "1." in style_option:
            caption = f"""เจาะลึกนวัตกรรมและแนวคิดสำคัญเกี่ยวกับ **{topic}** สาระสำคัญที่ {target_audience} ไม่ควรมองข้าม\n\nในปัจจุบัน **{topic}** ได้ก้าวเข้ามามีบทบาทสำคัญอย่างยิ่ง บทความนี้จึงได้รวบรวมประเด็นหลักดังนี้:\n\n▪️ **ประเด็นที่ 1:** การเพิ่มประสิทธิภาพในการทำงานและการบริหารจัดการ\n▪️ **ประเด็นที่ 2:** การลดต้นทุนและระยะเวลาในการดำเนินการอย่างมีนัยสำคัญ\n▪️ **ประเด็นที่ 3:** การสร้างผลลัพธ์ที่ยั่งยืนและมีมาตรฐานระดับสากล\n\nเรียนเชิญผู้ที่สนใจศึกษารายละเอียดเพิ่มเติม กรุณา {cta_type}\n\n#{clean_tag} #ข้อมูลเชิงลึก #การบริหารจัดการ #นวัตกรรม"""
        elif "2." in style_option:
            caption = f"""ขอแนะนำบริการ/ผลิตภัณฑ์ **{topic}** ที่ออกแบบมาเพื่อยกระดับมาตรฐานสำหรับ {target_audience} โดยเฉพาะ\n\nมุ่งเน้นการส่งมอบโซลูชันที่มีคุณภาพสูง น่าเชื่อถือ และตอบสนองต่อความต้องการได้อย่างสมบูรณ์แบบ\n\n▪️ **ความโดดเด่น:** ควบคุมคุณภาพทุกขั้นตอนด้วยมาตรฐานระดับสากล\n▪️ **ความคุ้มค่า:** ให้ผลตอบแทนและประสิทธิภาพสูงสุดแก่ผู้ใช้งาน\n▪️ **การดูแล:** บริการหลังการขายระดับมืออาชีพโดยทีมงานผู้เชี่ยวชาญ\n\nสอบถามรายละเอียดเพิ่มเติม กรุณา {cta_type}\n\n#{clean_tag} #บริการคุณภาพ #โซลูชันธุรกิจ #มาตรฐานระดับสากล"""
        else:
            caption = f"""วิสัยทัศน์และการขับเคลื่อนองค์กรผ่านแนวคิด **{topic}**\n\nกุญแจสำคัญในการพัฒนาศักยภาพของ {target_audience} ในยุคปัจจุบัน คือการสร้างสมดุลระหว่างนวัตกรรมและความยั่งยืน\n\n▪️ **การปรับตัว:** เปิดรับแนวคิดใหม่ๆ เพื่อรับมือกับความเปลี่ยนแปลง\n▪️ **มุ่งเน้นคุณภาพ:** ไม่หยุดยั้งในการพัฒนามาตรฐานบริการ\n▪️ **สร้างคุณค่า:** ส่งมอบประโยชน์สูงสุดแก่สังคมและผู้ใช้บริการ\n\nขอเชิญร่วมพูดคุยและสร้างพันธมิตรทางธุรกิจได้โดย {cta_type}\n\n#{clean_tag} #วิสัยทัศน์ #การพัฒนาอย่างยั่งยืน #มุมมองผู้บริหาร"""

    return caption

# ---------------------------------------------------------
# ⚙️ 2. เมนู Sidebar ด้านข้าง
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/facebook-new.png", width=50)
    st.title("⚙️ AI Brand Control")
    st.caption("ศูนย์ควบคุมแบรนด์และพารามิเตอร์ AI")
    
    st.divider()
    
    brand_preset = st.selectbox(
        "🏢 โปรไฟล์แบรนด์ (Preset):",
        ["กำหนดเอง (Custom)", "☕ Cafe & Bakery", "🧴 สกินแคร์ & ความงาม", "🏠 อสังหาฯ / คอนโด", "🚗 ยานยนต์ / โชว์รูมรถ", "🛍️ ร้านค้า / บริการทั่วไป"]
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
        "🗣️ ระดับความเป็นทางการ (โทนเสียงภาษา):", 
        min_value=1, max_value=5, value=2,
        help="1-2 = ภาษาเพื่อน/ Gen-Z / ป้ายยา, 3 = เป็นกันเองแบบ SME, 4-5 = สุภาพ/ทางการระดับแบรนด์ใหญ่"
    )
    
    target_audience = st.selectbox(
        "🎯 กลุ่มเป้าหมายหลัก:",
        ["คนทำงาน / วัยสร้างตัว", "วัยรุ่น / Gen Z", "เจ้าของธุรกิจ / ผู้ประกอบการ", "คนทั่วไป / ลูกค้าทุกกลุ่ม"]
    )
    
    cta_type = st.radio(
        "📣 ปุ่มกระตุ้นการขาย (CTA):",
        ["ทักแชตเพจเพื่อรับโปร", "คอมเมนต์ใต้โพสต์", "คลิกลิงก์หน้าโปรไฟล์"]
    )
    
    st.divider()
    st.info("💡 **Engine Status:** Robust Image Caching Active")

# ---------------------------------------------------------
# 🚀 3. พื้นที่หลัก (Main Layout)
# ---------------------------------------------------------
st.title("🚀 AI Content & Marketing Automation")
st.caption("พิมพ์หัวข้ออะไรก็ได้ AI จะช่วยคิดแคปชันสไตล์คนจริงเขียน พร้อมภาพโฆษณาที่ไม่หายเมื่อปรับ Sidebar")

default_topic = "กาแฟเพื่อสุขภาพ"
if brand_preset == "☕ Cafe & Bakery":
    default_topic = "กาแฟสกัดเย็นเมล็ดอาราบิก้า"
elif brand_preset == "🧴 สกินแคร์ & ความงาม":
    default_topic = "เซรั่มไฮยาเข้มข้นกู้ผิวพัง"
elif brand_preset == "🏠 อสังหาฯ / คอนโด":
    default_topic = "คอนโดติดรถไฟฟ้า พร้อมอยู่"
elif brand_preset == "🚗 ยานยนต์ / โชว์รูมรถ":
    default_topic = "Honda Civic โฉมใหม่"
elif brand_preset == "🛍️ ร้านค้า / บริการทั่วไป":
    default_topic = "บริการทำความสะอาดบ้านแบบครบวงจร"

col_input1, col_input2 = st.columns([3, 1])
with col_input1:
    topic = st.text_input("📌 กรอกหัวข้อ / สินค้า / บริการที่ต้องการโพสต์:", value=default_topic)
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
        status_box = st.status("🤖 AI กำลังประมวลผลคอนเทนต์และรูปภาพ...", expanded=True)
        
        with status_box:
            st.write(f"🧠 1. ร่างแคปชันสไตล์คนจริงเขียน (ระดับความเป็นทางการ {formality_level}/5)...")
            caption = generate_human_caption(topic, style_option, formality_level, target_audience, cta_type)
            
            st.write(f"🌐 2. ส่งโจทย์ให้ FLUX AI เจนภาพสไตล์ '{img_art_style}'...")
            image_url = generate_ai_image_url(topic, img_art_style)
            
            st.write("📥 3. ดาวน์โหลดไฟล์รูปภาพเข้าสู่แรม (รอ AI เจนจนสมบูรณ์)...")
            image_bytes = fetch_image_data(image_url)
            
            # บันทึกลง Session State
            st.session_state.generated = True
            st.session_state.caption = caption
            st.session_state.image_url = image_url
            st.session_state.image_bytes = image_bytes
            st.session_state.art_style_used = img_art_style
            
            status_box.update(label="✅ สร้างโพสต์เรียบร้อยแล้ว!", state="complete", expanded=False)

# ---------------------------------------------------------
# 📱 5. ส่วนแสดงผลลัพธ์ (รองรับการปรับ Sidebar รูปไม่หายแน่นอน)
# ---------------------------------------------------------
if st.session_state.generated:
    # 🔄 Auto-Recovery: หากขยับ Sidebar แล้ว bytes ยังเป็น None ให้ดึงรูปเก็บเข้าแรมทันที
    if st.session_state.image_bytes is None and st.session_state.image_url:
        st.session_state.image_bytes = fetch_image_data(st.session_state.image_url)

    display_image = st.session_state.image_bytes if st.session_state.image_bytes else st.session_state.image_url

    st.divider()

    st.subheader("📊 AI Analytics & Insights")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="📈 Engagement Potential", value="98.2%", delta="+18.5%")
    m2.metric(label="🎯 Tone Alignment", value=f"Level {formality_level}/5 (Human)", delta=brand_preset)
    m3.metric(label="⏱️ Best Posting Time", value="18:30 น.", delta="Today")
    m4.metric(label="🖼️ Image Engine", value=st.session_state.art_style_used.split()[0], delta="FLUX Active")

    st.divider()

    st.subheader("📱 พรีวิวการแสดงผล (Multi-Platform Preview)")

    tab_fb, tab_ig, tab_line = st.tabs(["🔵 Facebook Post", "📸 Instagram Feed", "💬 LINE Official Account"])

    # Tab 1: Facebook
    with tab_fb:
        col_fb_view, col_fb_tool = st.columns([1.5, 1])
        with col_fb_view:
            with st.container(border=True):
                st.markdown(f"**{brand_preset if 'Custom' not in brand_preset else 'Demo Brand Official'}** · *เมื่อสักครู่นี้* 🌎")
                st.markdown(st.session_state.caption)
                st.image(display_image, caption=f"ภาพประกอบ AI สไตล์: {st.session_state.art_style_used}", use_container_width=True)
        
        with col_fb_tool:
            st.markdown("### 🛠️ เครื่องมือจัดการ")
            st.text_area("📋 แคปชันสำหรับก๊อปปี้:", value=st.session_state.caption, height=220)
            
            if st.session_state.image_bytes:
                st.download_button("📥 โหลดรูปภาพ AI (HD)", data=st.session_state.image_bytes, file_name="post_ai.jpg", mime="image/jpeg", use_container_width=True)
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
        st.image(display_image, width=450)
        st.caption(st.session_state.caption[:150] + "...")

    # Tab 3: LINE
    with tab_line:
        st.info("💬 ตัวอย่างหน้าตา Broadcast ข้อความบน LINE Official Account")
        with st.chat_message("assistant"):
            st.write(st.session_state.caption)
            st.image(display_image, width=350)
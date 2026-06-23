<<<<<<< HEAD
# =========================================================
# 🍄 AI MUSHROOM DETECTION SYSTEM
# PREMIUM MODERN VERSION
# =========================================================

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Mushroom Detection",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME TOGGLE
# =========================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_toggle = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=(st.session_state.theme == "dark")
)

if theme_toggle:
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

if st.session_state.theme == "dark":

    bg_main = "#0f172a"
    bg_secondary = "#111827"

    card_bg = "rgba(30,41,59,0.75)"

    text_primary = "#f8fafc"
    text_secondary = "#94a3b8"

    border_color = "rgba(255,255,255,0.08)"

    gradient_1 = "#6366f1"
    gradient_2 = "#8b5cf6"

else:

    bg_main = "#f8fafc"
    bg_secondary = "#e2e8f0"

    card_bg = "rgba(255,255,255,0.85)"

    text_primary = "#0f172a"
    text_secondary = "#64748b"

    border_color = "rgba(15,23,42,0.08)"

    gradient_1 = "#4f46e5"
    gradient_2 = "#7c3aed"

# =========================================================
# THEME COLOR
# =========================================================

if st.session_state.theme == "dark":

    bg_main = "#0f172a"
    bg_secondary = "#111827"
    card_bg = "rgba(30,41,59,0.75)"
    text_primary = "#f8fafc"
    text_secondary = "#cbd5e1"
    border_color = "rgba(255,255,255,0.08)"

    gradient_1 = "#6366f1"
    gradient_2 = "#8b5cf6"

else:

    bg_main = "#f1f5f9"
    bg_secondary = "#e2e8f0"
    card_bg = "rgba(255,255,255,0.80)"
    text_primary = "#0f172a"
    text_secondary = "#475569"
    border_color = "rgba(15,23,42,0.08)"

    gradient_1 = "#4f46e5"
    gradient_2 = "#7c3aed"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background:
    linear-gradient(
        135deg,
        {bg_main},
        {bg_secondary}
    );
    color: {text_primary};
}}

/* ============================= */
/* SIDEBAR */
/* ============================= */

section[data-testid="stSidebar"] {{
    background: {card_bg};
    backdrop-filter: blur(20px);
    border-right: 1px solid {border_color};
}}

section[data-testid="stSidebar"] * {{
    color: {text_primary} !important;
}}

/* ============================= */
/* TITLE */
/* ============================= */

.main-title {{
    font-size: 52px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(
        to right,
        {gradient_1},
        {gradient_2}
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    color: {text_secondary};
    font-size: 18px;
    margin-bottom: 10px;
}}

/* ============================= */
/* GLASS CARD */
/* ============================= */

.glass {{
    background: {card_bg};
    backdrop-filter: blur(18px);
    border: 1px solid {border_color};
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 20px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.12);
}}

/* ============================= */
/* METRIC CARD */
/* ============================= */

.metric-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 20px;
    padding: 18px;
    text-align: center;
}}

/* ============================= */
/* BUTTON */
/* ============================= */

.stButton > button {{
    width: 100%;
    border: none;
    border-radius: 14px;

    padding: 12px;

    background:
    linear-gradient(
        90deg,
        {gradient_1},
        {gradient_2}
    );

    color: white;

    font-weight: 600;
    font-size: 15px;

    transition: 0.3s;
}}

.stButton > button:hover {{
    transform: scale(1.02);
    opacity: 0.92;
}}

/* ============================= */
/* DOWNLOAD BUTTON */
/* ============================= */

.stDownloadButton > button {{
    width: 100%;
    border: none;
    border-radius: 14px;

    padding: 12px;

    background:
    linear-gradient(
        90deg,
        #3b82f6,
        #2563eb
    );

    color: white;

    font-weight: 600;
    font-size: 15px;

    transition: 0.3s;
}}

.stDownloadButton > button:hover {{
    transform: scale(1.02);
}}

/* ============================= */
/* FILE UPLOADER */
/* ============================= */

[data-testid="stFileUploader"] {{
    background: {card_bg};
    border: 1px dashed {border_color};
    border-radius: 18px;
    padding: 10px;
}}

/* ============================= */
/* TABS */
/* ============================= */

.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
}}

.stTabs [data-baseweb="tab"] {{
    background: {card_bg};
    border-radius: 14px;
    padding: 10px 18px;
    color: {text_primary};
}}

.stTabs [aria-selected="true"] {{
    background:
    linear-gradient(
        90deg,
        {gradient_1},
        {gradient_2}
    );

    color: white !important;
}}

/* ============================= */
/* DATAFRAME */
/* ============================= */

[data-testid="stDataFrame"] {{
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid {border_color};
}}

/* ============================= */
/* CONFIDENCE BADGE */
/* ============================= */

.confidence-high {{
    background: rgba(34,197,94,0.18);
    border: 1px solid #22c55e;
    color: #22c55e;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

.confidence-medium {{
    background: rgba(234,179,8,0.18);
    border: 1px solid #eab308;
    color: #eab308;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

.confidence-low {{
    background: rgba(239,68,68,0.18);
    border: 1px solid #ef4444;
    color: #ef4444;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

/* ============================= */
/* IMAGE */
/* ============================= */

img {{
    border-radius: 20px;
}}

/* ============================= */
/* RESPONSIVE */
/* ============================= */

@media (max-width: 768px) {{

    .main-title {{
        font-size: 34px;
    }}

    .subtitle {{
        font-size: 15px;
    }}

    .glass {{
        padding: 16px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = YOLO("best.pt")

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:

    st.session_state.history = {
        "Jamur Baby Champignon": 0,
        "Jamur Enoki": 0,
        "Jamur Kuping": 0,
        "Jamur Salju": 0,
        "jamur tiram": 0
    }

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ AI Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.01,
    1.0,
    0.10
)

st.sidebar.markdown("---")

st.sidebar.markdown("## 🍄 Supported Mushrooms")

st.sidebar.success("Baby Champignon")
st.sidebar.success("Enoki")
st.sidebar.success("Kuping")
st.sidebar.success("Salju")
st.sidebar.success("Jamur Tiram")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Reset Statistik"):

    st.session_state.history = {
        "Jamur Baby Champignon": 0,
        "Jamur Enoki": 0,
        "Jamur Kuping": 0,
        "Jamur Salju": 0,
        "jamur tiram": 0
    }

    st.rerun()

# =========================================================
# PREMIUM HEADER
# =========================================================

st.markdown(f"""
<div style="
background:{card_bg};
padding:40px;
border-radius:30px;
border:1px solid {border_color};
backdrop-filter:blur(20px);
text-align:center;
margin-bottom:25px;
box-shadow:0 8px 32px rgba(0,0,0,0.15);
">

<div style="
letter-spacing:4px;
font-size:14px;
font-weight:600;
color:{text_secondary};
">
ARTIFICIAL INTELLIGENCE SYSTEM
</div>

<div style="
font-size:50px;
font-weight:800;
color:{text_primary};
margin-top:10px;
">
🍄 Mushroom Detection 🍄
</div>

<div style="
font-size:18px;
color:{text_secondary};
margin-top:12px;
">
YOLOv8-Based Intelligent Mushroom Classification Platform
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "📤 Upload Image",
    "📷 Webcam Realtime"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Mushroom Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.image(
                image,
                caption="🖼 Input Image",
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # SAVE TEMP FILE
        # =========================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp_file:

            image.save(temp_file.name)

            temp_path = temp_file.name

        # =========================================================
        # LOADING ANIMATION
        # =========================================================

        with st.spinner("🤖 AI sedang menganalisis gambar..."):

            results = model(
                temp_path,
                conf=confidence
            )

        result = results[0]

        annotated = result.plot()

        # =========================================================
        # AUTO SAVE RESULT
        # =========================================================

        os.makedirs("hasil_deteksi", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        save_path = f"hasil_deteksi/deteksi_{timestamp}.jpg"

        cv2.imwrite(
            save_path,
            cv2.cvtColor(
                annotated,
                cv2.COLOR_RGB2BGR
            )
        )

        with col2:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.image(
                annotated,
                caption="🎯 Detection Result",
                use_container_width=True
            )

            st.success(f"📸 Otomatis tersimpan")

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # DETECTION STATS
        # =========================================================

        class_counts = st.session_state.history

        confidences = []

        if len(result.boxes) > 0:

            for box in result.boxes:

                cls_id = int(box.cls[0])

                class_name = model.names[cls_id]

                conf_value = float(box.conf[0])

                confidences.append(conf_value)

                if class_name not in class_counts:
                    class_counts[class_name] = 0

                class_counts[class_name] += 1

            # =====================================================
            # CONFIDENCE BADGE
            # =====================================================

            avg_conf = np.mean(confidences)

            if avg_conf > 0.8:

                badge = "confidence-high"

            elif avg_conf > 0.5:

                badge = "confidence-medium"

            else:

                badge = "confidence-low"

            st.markdown(f"""
            <div class="{badge}">
                🎯 Average Confidence:
                {avg_conf:.2f}
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # =====================================================
            # METRICS
            # =====================================================

            colA, colB, colC = st.columns(3)

            with colA:
                st.metric(
                    "Jenis Terdeteksi",
                    len(class_counts)
                )

            with colB:
                st.metric(
                    "Total Deteksi",
                    sum(class_counts.values())
                )

            with colC:
                st.metric(
                    "Confidence",
                    f"{avg_conf:.2f}"
                )

            # =====================================================
            # TABLE
            # =====================================================

            st.markdown("## 📊 Detection Statistics")

            df = pd.DataFrame({
                "Jenis Jamur": list(class_counts.keys()),
                "Jumlah": list(class_counts.values())
            })

            st.dataframe(
                df,
                use_container_width=True
            )

            # =====================================================
            # EXPORT CSV
            # =====================================================

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download CSV",
                csv,
                "hasil_deteksi.csv",
                "text/csv"
            )

        else:

            st.error("❌ Tidak ada jamur terdeteksi")

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown("## 📷 Webcam Detection")

    run = st.checkbox("Aktifkan Webcam")

    FRAME_WINDOW = st.image([])

    camera = cv2.VideoCapture(0)

    while run:

        success, frame = camera.read()

        if not success:
            st.error("❌ Webcam tidak ditemukan")
            break

        results = model(
            frame,
            conf=confidence
        )

        annotated_frame = results[0].plot()

        FRAME_WINDOW.image(
            cv2.cvtColor(
                annotated_frame,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

    camera.release()

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<center>

### 🍄 AI Mushroom Detection Dashboard

🎯Smart Detection System using YOLOv8🎯

</center>
=======
# =========================================================
# 🍄 AI MUSHROOM DETECTION SYSTEM
# PREMIUM MODERN VERSION
# =========================================================

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Mushroom Detection",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME TOGGLE
# =========================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_toggle = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=(st.session_state.theme == "dark")
)

if theme_toggle:
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

if st.session_state.theme == "dark":

    bg_main = "#0f172a"
    bg_secondary = "#111827"

    card_bg = "rgba(30,41,59,0.75)"

    text_primary = "#f8fafc"
    text_secondary = "#94a3b8"

    border_color = "rgba(255,255,255,0.08)"

    gradient_1 = "#6366f1"
    gradient_2 = "#8b5cf6"

else:

    bg_main = "#f8fafc"
    bg_secondary = "#e2e8f0"

    card_bg = "rgba(255,255,255,0.85)"

    text_primary = "#0f172a"
    text_secondary = "#64748b"

    border_color = "rgba(15,23,42,0.08)"

    gradient_1 = "#4f46e5"
    gradient_2 = "#7c3aed"

# =========================================================
# THEME COLOR
# =========================================================

if st.session_state.theme == "dark":

    bg_main = "#0f172a"
    bg_secondary = "#111827"
    card_bg = "rgba(30,41,59,0.75)"
    text_primary = "#f8fafc"
    text_secondary = "#cbd5e1"
    border_color = "rgba(255,255,255,0.08)"

    gradient_1 = "#6366f1"
    gradient_2 = "#8b5cf6"

else:

    bg_main = "#f1f5f9"
    bg_secondary = "#e2e8f0"
    card_bg = "rgba(255,255,255,0.80)"
    text_primary = "#0f172a"
    text_secondary = "#475569"
    border_color = "rgba(15,23,42,0.08)"

    gradient_1 = "#4f46e5"
    gradient_2 = "#7c3aed"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background:
    linear-gradient(
        135deg,
        {bg_main},
        {bg_secondary}
    );
    color: {text_primary};
}}

/* ============================= */
/* SIDEBAR */
/* ============================= */

section[data-testid="stSidebar"] {{
    background: {card_bg};
    backdrop-filter: blur(20px);
    border-right: 1px solid {border_color};
}}

section[data-testid="stSidebar"] * {{
    color: {text_primary} !important;
}}

/* ============================= */
/* TITLE */
/* ============================= */

.main-title {{
    font-size: 52px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(
        to right,
        {gradient_1},
        {gradient_2}
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    color: {text_secondary};
    font-size: 18px;
    margin-bottom: 10px;
}}

/* ============================= */
/* GLASS CARD */
/* ============================= */

.glass {{
    background: {card_bg};
    backdrop-filter: blur(18px);
    border: 1px solid {border_color};
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 20px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.12);
}}

/* ============================= */
/* METRIC CARD */
/* ============================= */

.metric-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 20px;
    padding: 18px;
    text-align: center;
}}

/* ============================= */
/* BUTTON */
/* ============================= */

.stButton > button {{
    width: 100%;
    border: none;
    border-radius: 14px;

    padding: 12px;

    background:
    linear-gradient(
        90deg,
        {gradient_1},
        {gradient_2}
    );

    color: white;

    font-weight: 600;
    font-size: 15px;

    transition: 0.3s;
}}

.stButton > button:hover {{
    transform: scale(1.02);
    opacity: 0.92;
}}

/* ============================= */
/* DOWNLOAD BUTTON */
/* ============================= */

.stDownloadButton > button {{
    width: 100%;
    border: none;
    border-radius: 14px;

    padding: 12px;

    background:
    linear-gradient(
        90deg,
        #3b82f6,
        #2563eb
    );

    color: white;

    font-weight: 600;
    font-size: 15px;

    transition: 0.3s;
}}

.stDownloadButton > button:hover {{
    transform: scale(1.02);
}}

/* ============================= */
/* FILE UPLOADER */
/* ============================= */

[data-testid="stFileUploader"] {{
    background: {card_bg};
    border: 1px dashed {border_color};
    border-radius: 18px;
    padding: 10px;
}}

/* ============================= */
/* TABS */
/* ============================= */

.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
}}

.stTabs [data-baseweb="tab"] {{
    background: {card_bg};
    border-radius: 14px;
    padding: 10px 18px;
    color: {text_primary};
}}

.stTabs [aria-selected="true"] {{
    background:
    linear-gradient(
        90deg,
        {gradient_1},
        {gradient_2}
    );

    color: white !important;
}}

/* ============================= */
/* DATAFRAME */
/* ============================= */

[data-testid="stDataFrame"] {{
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid {border_color};
}}

/* ============================= */
/* CONFIDENCE BADGE */
/* ============================= */

.confidence-high {{
    background: rgba(34,197,94,0.18);
    border: 1px solid #22c55e;
    color: #22c55e;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

.confidence-medium {{
    background: rgba(234,179,8,0.18);
    border: 1px solid #eab308;
    color: #eab308;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

.confidence-low {{
    background: rgba(239,68,68,0.18);
    border: 1px solid #ef4444;
    color: #ef4444;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}}

/* ============================= */
/* IMAGE */
/* ============================= */

img {{
    border-radius: 20px;
}}

/* ============================= */
/* RESPONSIVE */
/* ============================= */

@media (max-width: 768px) {{

    .main-title {{
        font-size: 34px;
    }}

    .subtitle {{
        font-size: 15px;
    }}

    .glass {{
        padding: 16px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = YOLO("best.pt")

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:

    st.session_state.history = {
        "Jamur Baby Champignon": 0,
        "Jamur Enoki": 0,
        "Jamur Kuping": 0,
        "Jamur Salju": 0,
        "jamur tiram": 0
    }

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ AI Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.01,
    1.0,
    0.10
)

st.sidebar.markdown("---")

st.sidebar.markdown("## 🍄 Supported Mushrooms")

st.sidebar.success("Baby Champignon")
st.sidebar.success("Enoki")
st.sidebar.success("Kuping")
st.sidebar.success("Salju")
st.sidebar.success("Jamur Tiram")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Reset Statistik"):

    st.session_state.history = {
        "Jamur Baby Champignon": 0,
        "Jamur Enoki": 0,
        "Jamur Kuping": 0,
        "Jamur Salju": 0,
        "jamur tiram": 0
    }

    st.rerun()

# =========================================================
# PREMIUM HEADER
# =========================================================

st.markdown(f"""
<div style="
background:{card_bg};
padding:40px;
border-radius:30px;
border:1px solid {border_color};
backdrop-filter:blur(20px);
text-align:center;
margin-bottom:25px;
box-shadow:0 8px 32px rgba(0,0,0,0.15);
">

<div style="
letter-spacing:4px;
font-size:14px;
font-weight:600;
color:{text_secondary};
">
ARTIFICIAL INTELLIGENCE SYSTEM
</div>

<div style="
font-size:50px;
font-weight:800;
color:{text_primary};
margin-top:10px;
">
🍄 Mushroom Detection 🍄
</div>

<div style="
font-size:18px;
color:{text_secondary};
margin-top:12px;
">
YOLOv8-Based Intelligent Mushroom Classification Platform
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "📤 Upload Image",
    "📷 Webcam Realtime"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Mushroom Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.image(
                image,
                caption="🖼 Input Image",
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # SAVE TEMP FILE
        # =========================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp_file:

            image.save(temp_file.name)

            temp_path = temp_file.name

        # =========================================================
        # LOADING ANIMATION
        # =========================================================

        with st.spinner("🤖 AI sedang menganalisis gambar..."):

            results = model(
                temp_path,
                conf=confidence
            )

        result = results[0]

        annotated = result.plot()

        # =========================================================
        # AUTO SAVE RESULT
        # =========================================================

        os.makedirs("hasil_deteksi", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        save_path = f"hasil_deteksi/deteksi_{timestamp}.jpg"

        cv2.imwrite(
            save_path,
            cv2.cvtColor(
                annotated,
                cv2.COLOR_RGB2BGR
            )
        )

        with col2:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.image(
                annotated,
                caption="🎯 Detection Result",
                use_container_width=True
            )

            st.success(f"📸 Otomatis tersimpan")

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # DETECTION STATS
        # =========================================================

        class_counts = st.session_state.history

        confidences = []

        if len(result.boxes) > 0:

            for box in result.boxes:

                cls_id = int(box.cls[0])

                class_name = model.names[cls_id]

                conf_value = float(box.conf[0])

                confidences.append(conf_value)

                if class_name not in class_counts:
                    class_counts[class_name] = 0

                class_counts[class_name] += 1

            # =====================================================
            # CONFIDENCE BADGE
            # =====================================================

            avg_conf = np.mean(confidences)

            if avg_conf > 0.8:

                badge = "confidence-high"

            elif avg_conf > 0.5:

                badge = "confidence-medium"

            else:

                badge = "confidence-low"

            st.markdown(f"""
            <div class="{badge}">
                🎯 Average Confidence:
                {avg_conf:.2f}
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # =====================================================
            # METRICS
            # =====================================================

            colA, colB, colC = st.columns(3)

            with colA:
                st.metric(
                    "Jenis Terdeteksi",
                    len(class_counts)
                )

            with colB:
                st.metric(
                    "Total Deteksi",
                    sum(class_counts.values())
                )

            with colC:
                st.metric(
                    "Confidence",
                    f"{avg_conf:.2f}"
                )

            # =====================================================
            # TABLE
            # =====================================================

            st.markdown("## 📊 Detection Statistics")

            df = pd.DataFrame({
                "Jenis Jamur": list(class_counts.keys()),
                "Jumlah": list(class_counts.values())
            })

            st.dataframe(
                df,
                use_container_width=True
            )

            # =====================================================
            # EXPORT CSV
            # =====================================================

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download CSV",
                csv,
                "hasil_deteksi.csv",
                "text/csv"
            )

        else:

            st.error("❌ Tidak ada jamur terdeteksi")

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown("## 📷 Webcam Detection")

    run = st.checkbox("Aktifkan Webcam")

    FRAME_WINDOW = st.image([])

    camera = cv2.VideoCapture(0)

    while run:

        success, frame = camera.read()

        if not success:
            st.error("❌ Webcam tidak ditemukan")
            break

        results = model(
            frame,
            conf=confidence
        )

        annotated_frame = results[0].plot()

        FRAME_WINDOW.image(
            cv2.cvtColor(
                annotated_frame,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

    camera.release()

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<center>

### 🍄 AI Mushroom Detection Dashboard

🎯Smart Detection System using YOLOv8🎯

</center>
>>>>>>> 56ff73b58d7ef8f30ed90529e5e050b8c72d3320
""", unsafe_allow_html=True)
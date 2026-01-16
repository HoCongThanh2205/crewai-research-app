import streamlit as st
import time
import base64
import json
import os
from datetime import datetime
from main import run_crew_process

# Cấu hình trang
st.set_page_config(
    page_title="Bệnh Viện 199 - AI Research",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HISTORY FUNCTIONS ---
HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_to_history(topic, result):
    history = load_history()
    # Tạo object mới
    new_entry = {
        "topic": topic,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result
    }
    # Thêm vào đầu danh sách
    history.insert(0, new_entry)
    # Giữ lại 20 mục gần nhất
    history = history[:20]
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# --- END HISTORY FUNCTIONS ---

# Hàm load ảnh background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    header_bg_base64 = get_base64_of_bin_file("assets/header_bg.jpg")
except:
    header_bg_base64 = ""

# Custom CSS cho giao diện Bệnh viện/Y tế
st.markdown(f"""
<style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Nền chung - Xanh bệnh viện nhạt */
    .stApp {{
        background-color: #E0F2F1; /* Teal 50 - Rất nhạt */
        background-image: linear-gradient(to bottom right, #E0F2F1, #B2DFDB);
    }}

    /* Header Container với ảnh nền */
    .header-container {{
        background-image: url("data:image/jpg;base64,{header_bg_base64}");
        background-size: 100% 100%;
        background-position: center;
        padding: 80px 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    .header-title h1 {{
        color: #FFFFFF !important;
        margin: 0;
        font-size: 2.5rem;
    }}
    
    .header-subtitle {{
        color: #E0F7FA;
        font-size: 1.2rem;
        font-weight: 500;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid #B2DFDB;
    }}

    /* Input Field */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 2px solid #009688; /* Teal chính */
        padding: 10px;
        background-color: white;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #004D40;
        box-shadow: 0 0 0 2px rgba(0, 150, 136, 0.2);
    }}

    /* Button */
    .stButton > button {{
        background-color: #00796B; /* Teal đậm hơn */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #004D40;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }}

    /* Cards / Containers */
    .css-1r6slb0, .stTabs {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 150, 136, 0.1);
        border: 1px solid #B2DFDB;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: #E0F2F1;
        border-radius: 8px 8px 0 0;
        color: #00695C;
        font-weight: 600;
        border: 1px solid transparent;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        color: #004D40 !important;
        border-top: 3px solid #009688;
        border-bottom: none;
    }}

</style>
""", unsafe_allow_html=True)

# Header Custom
st.markdown("""
<div class="header-container">
    <div class="header-title">
        <h1>Hệ Thống Nghiên Cứu Y Tế</h1>
        <div class="header-subtitle">Hỗ trợ chuyên môn Bệnh viện 199</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State for History Selection
if 'selected_history_item' not in st.session_state:
    st.session_state.selected_history_item = None

# Logo ở Sidebar (thay vì header để đỡ rối với ảnh nền)
with st.sidebar:
    try:
        st.image("assets/logo.png", use_container_width=True)
    except:
        st.warning("Chưa có logo")
    
    st.markdown("---")
    st.header("⚙️ Bảng Điều Khiển")
    st.info("Nhập chủ đề y tế hoặc bệnh học để AI tiến hành phân tích chuyên sâu.")

    # --- HISTORY SECTION ---
    st.markdown("---")
    st.header("🕒 Lịch sử nghiên cứu")
    history_data = load_history()
    
    if not history_data:
        st.caption("Chưa có lịch sử nào.")
    else:
        for idx, item in enumerate(history_data):
            # Tạo label gồm tên topic và ngày
            label = f"{item['topic']}\n({item['timestamp']})"
            if st.button(label, key=f"hist_{idx}", use_container_width=True):
                st.session_state.selected_history_item = item
                st.rerun() # Reload lại trang để hiển thị kết quả
    # --- END HISTORY SECTION ---

# Main Input Area
st.markdown("### 🔍 Nhập chủ đề nghiên cứu")
topic = st.text_input("", placeholder="Ví dụ: Ứng dụng AI trong chẩn đoán ung thư phổi...", label_visibility="collapsed")

col_btn, col_space = st.columns([1, 4])
with col_btn:
    start_btn = st.button("🚀 Bắt đầu phân tích", type="primary", use_container_width=True)

# Logic hiển thị kết quả
results = None

# Case 1: Người dùng bấm chạy mới
if start_btn and topic:
    st.session_state.selected_history_item = None # Clear history selection
    
    # Progress Area
    status_container = st.container()
    with status_container:
        st.markdown("### ⏳ Đang xử lý...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Đang tìm kiếm tài liệu y khoa uy tín...",
            "Đang phân tích dữ liệu lâm sàng...",
            "Đang tổng hợp xu hướng điều trị mới...",
            "Đang soạn thảo báo cáo chuyên môn...",
            "Đang tạo Timeline sự kiện..."
        ]
        
        # Giả lập hiệu ứng loading ban đầu
        for i, step in enumerate(steps):
            status_text.text(f"🔄 {step}")
            progress_bar.progress((i + 1) * 5)
            time.sleep(0.3)

    try:
        # Chạy CrewAI
        with st.spinner('🤖 Đội ngũ AI đang làm việc hết công suất...'):
            results = run_crew_process(topic)
        
        # Lưu vào lịch sử
        save_to_history(topic, results)
        
        progress_bar.progress(100)
        status_text.success("✅ Phân tích hoàn tất!")
        time.sleep(1)
        status_container.empty() # Ẩn thanh loading sau khi xong

    except Exception as e:
        st.error(f"❌ Đã xảy ra lỗi hệ thống: {e}")

# Case 2: Người dùng chọn từ lịch sử
elif st.session_state.selected_history_item:
    results = st.session_state.selected_history_item['result']
    st.info(f"📂 Đang xem lại kết quả: **{st.session_state.selected_history_item['topic']}** (Ngày tạo: {st.session_state.selected_history_item['timestamp']})")

elif start_btn and not topic:
    st.warning("⚠️ Vui lòng nhập chủ đề để bắt đầu!")


# Hiển thị kết quả (chung cho cả 2 case)
if results:
    # Hiển thị kết quả dạng Card/Tabs
    st.markdown("## 📑 Kết quả Phân tích")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Nghiên cứu", 
        "🧠 Phân tích", 
        "📈 Xu hướng", 
        "✍️ Báo cáo",
        "⏱️ Timeline"
    ])
    
    with tab1:
        st.markdown("### 🏥 Tổng hợp Nghiên cứu")
        st.markdown(results["research"])
    
    with tab2:
        st.markdown("### 🔬 Phân tích Chuyên sâu")
        st.markdown(results["analysis"])
        
    with tab3:
        st.markdown("### 📊 Xu hướng & Dư luận")
        st.markdown(results["trend"])
        
    with tab4:
        st.markdown("### 📝 Nội dung Truyền thông")
        st.markdown(results["content"])
        
    with tab5:
        timeline_url = results.get("timeline_url")
        if timeline_url:
            st.success("🎉 Đã tạo Timeline thành công!")
            st.markdown(f"""
            <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #2196F3;">
                <h3>⏱️ Timeline Sự Kiện</h3>
                <p>Bấm vào nút bên dưới để xem chi tiết timeline tương tác.</p>
                <a href="{timeline_url}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #1976D2; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
                        👉 Xem Timeline Ngay
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Không có dữ liệu Timeline hoặc đang xử lý.")
            if results.get("timeline"):
                st.json(results.get("timeline"))

    # Footer status
    if "sheets_status" in results:
        st.toast(f"Dữ liệu đã được lưu vào Google Sheets! (Status: {results.get('sheets_status')})", icon="✅")

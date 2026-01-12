import streamlit as st
import time
from main import run_crew_process

st.set_page_config(
    page_title="CrewAI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CrewAI Research Assistant")
st.markdown("Hệ thống tự động nghiên cứu, phân tích và tạo nội dung.")

# Sidebar
with st.sidebar:
    st.header("Cấu hình")
    st.info("Nhập chủ đề bên phải và nhấn 'Bắt đầu' để chạy đội ngũ AI.")

# Main Input
topic = st.text_input("Nhập chủ đề cần nghiên cứu:", placeholder="Ví dụ: Tương lai của AI trong y tế")

if st.button("🚀 Bắt đầu nghiên cứu", type="primary"):
    if not topic:
        st.warning("Vui lòng nhập chủ đề!")
    else:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        status_text.text("⏳ Đang khởi động CrewAI...")
        progress_bar.progress(10)
        
        try:
            # Vì CrewAI chạy đồng bộ, ta dùng spinner
            with st.spinner('Đang thực hiện nghiên cứu, phân tích và viết bài... (Quá trình này có thể mất vài phút)'):
                results = run_crew_process(topic)
            
            progress_bar.progress(100)
            status_text.success("✅ Hoàn thành!")
            
            # Hiển thị kết quả
            st.divider()
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🔍 Research", 
                "🧠 Analysis", 
                "📈 Trends", 
                "✍️ Content",
                "⏱️ Timeline"
            ])
            
            with tab1:
                st.markdown(results["research"])
            
            with tab2:
                st.markdown(results["analysis"])
                
            with tab3:
                st.markdown(results["trend"])
                
            with tab4:
                st.markdown(results["content"])
                
            with tab5:
                timeline_url = results.get("timeline_url")
                if timeline_url:
                    st.success("🎉 Tạo Timeline thành công!")
                    st.markdown(f"### [👉 Bấm vào đây để xem Timeline]({timeline_url})")
                    st.caption(f"Link: {timeline_url}")
                else:
                    st.info("Không có dữ liệu Timeline hoặc đang xử lý.")
                    if results.get("timeline"):
                        st.json(results.get("timeline"))

            st.success(f"Dữ liệu đã được lưu vào Google Sheets! (Status: {results.get('sheets_status')})")

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

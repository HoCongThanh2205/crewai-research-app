import requests
import time
import PyPDF2
import docx
import io
from crew import build_crew
from tasks import research_task, analysis_task, trend_task, content_task
from tools.google_sheets_writer import write_to_google_sheets

def read_pdf(file_stream):
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def read_docx(file_stream):
    try:
        doc = docx.Document(file_stream)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def run_crew_process(topic: str, file_content: str = None, file_name: str = None):
    """
    Chạy toàn bộ quy trình CrewAI và các tool tích hợp.
    Trả về dictionary chứa kết quả.
    """
    print(f"🚀 Bắt đầu xử lý chủ đề: {topic}")
    
    # Nếu có file, cập nhật description của research_task
    if file_content:
        print(f"📂 Đã nhận file: {file_name}")
        research_task.description = f"""
        CONTEXT FROM UPLOADED FILE ({file_name}):
        {file_content[:20000]} # Limit 20k chars to avoid token limit
        
        TASK:
        1. Analyze the uploaded document content above carefully.
        2. Research the topic: "{topic}" using the Search Tool.
        3. Combine insights from the file AND external search results.
        
        Requirements:
        - Find the latest and most relevant information.
        - **CRITICAL**: Every piece of information MUST have a citation with a valid URL.
        - Format citations as: [Source Name](URL)
        - If you cannot find a URL, explicitly state that.
        - Neutral, factual tone.
        - Write in VIETNAMESE.
        """
    else:
        # Reset description nếu không có file (để tránh lưu state cũ)
        research_task.description = f"""
        Research the topic: "{topic}" using the Search Tool.

        Requirements:
        - Find the latest and most relevant information.
        - **CRITICAL**: Every piece of information MUST have a citation with a valid URL.
        - Format citations as: [Source Name](URL)
        - If you cannot find a URL, explicitly state that.
        - Neutral, factual tone.
        - Write in VIETNAMESE.
        """

    crew = build_crew(topic)
    crew.kickoff()

    # 🔥 LẤY OUTPUT GỐC – KHÔNG BỊ TÓM TẮT
    research_output = research_task.output.raw
    analysis_output = analysis_task.output.raw
    trend_output = trend_task.output.raw
    content_output = content_task.output.raw

    # ========= 1️⃣ POST FORM-DATA =========
    upload_url = "https://tool.taivo.top/notebooklm/upload"

    def remove_non_bmp_characters(text):
        return ''.join(c for c in text if ord(c) <= 0xFFFF)

    def clean_output(text):
        """Loại bỏ các dòng log của tool (Using tool, Parameters) khỏi output"""
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Loại bỏ dòng chứa log tool
            if "Using tool:" in line or "Parameters:" in line or "Using tool" in line:
                continue
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines).strip()

    # 🔥 LẤY OUTPUT GỐC – KHÔNG BỊ TÓM TẮT
    research_output = research_task.output.raw
    analysis_output = analysis_task.output.raw
    trend_output = clean_output(trend_task.output.raw) # Clean logs
    content_output = content_task.output.raw

    # Filter emojis/non-BMP chars for this specific API to avoid ChromeDriver error
    sanitized_content = remove_non_bmp_characters(content_output)

    form_data = {
        "text": sanitized_content,
        "prompt": "Dựa trên toàn bộ tài liệu đã tải lên, hãy tạo một timeline"
    }

    try:
        upload_response = requests.post(
            upload_url,
            data=form_data,  # ← form-data
            timeout=30
        )
        print("Upload status:", upload_response.status_code)
        
        upload_json = upload_response.json()
        job_id = upload_json.get("job_id")
        
        timeline_result = None
        
        if job_id:
            print("✅ job_id:", job_id)
            # ========= 2️⃣ ĐỢI XỬ LÝ =========
            time.sleep(10)  # API này xử lý khá lâu

            # ========= 3️⃣ GET RESULT =========
            result_url = f"https://tool.taivo.top/notebooklm/result/{job_id}"
            
            # Thử tối đa 10 lần (100s)
            for _ in range(10):
                try:
                    result_response = requests.get(result_url, timeout=30)
                    result_json = result_response.json()
                    print("📡 RESULT:", result_json)

                    if result_json.get("status") == "running":
                        print("⏳ Đang xử lý... đợi 10 giây")
                        time.sleep(10)
                        continue
                    
                    # Nếu đã xong
                    print("🎉 HOÀN THÀNH TIMELINE")
                    timeline_result = result_json
                    break
                except Exception as e:
                    print(f"⚠️ Lỗi khi check result: {e}")
                    time.sleep(5)
        else:
            print("❌ Không lấy được job_id cho Timeline")

    except Exception as e:
        print(f"⚠️ Lỗi quá trình tạo Timeline: {e}")
        timeline_result = {"error": str(e)}

    # Lấy URL timeline (nếu có)
    timeline_url = ""
    if timeline_result:
        print(f"🔍 DEBUG TIMELINE RESULT: {timeline_result}") # Debug
        if "result" in timeline_result:
            timeline_url = timeline_result["result"]
            print(f"✅ FOUND TIMELINE URL: {timeline_url}")
        else:
            print("⚠️ Timeline result does not contain 'result' key")
    else:
        print("⚠️ No timeline result returned")

    # 🔥 LƯU TẠI PYTHON (KHÔNG QUA AGENT)
    try:
        sheets_status = write_to_google_sheets(
            topic=topic,
            research=research_output,
            analysis=analysis_output,
            trend=trend_output,
            content=content_output,
            timeline=timeline_url
        )
        print(f"✅ Đã lưu vào Google Sheets (Status: {sheets_status})")
    except Exception as e:
        print(f"❌ Lỗi lưu Google Sheets: {e}")
        sheets_status = "Error"

    return {
        "topic": topic,
        "research": research_output,
        "analysis": analysis_output,
        "trend": trend_output,
        "content": content_output,
        "timeline": timeline_result,
        "timeline_url": timeline_url,
        "sheets_status": sheets_status
    }

if __name__ == "__main__":
    topic_input = input("Nhập chủ đề: ")
    run_crew_process(topic_input)

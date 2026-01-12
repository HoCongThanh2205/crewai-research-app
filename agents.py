from crewai import Agent
from llms import gemini_llm, claude_llm, chatgpt_llm, grok_llm

research_agent = Agent(
    role="Research Specialist",
    goal="Tìm kiếm thông tin đa nguồn bằng TIẾNG VIỆT, có trích dẫn",
    backstory=(
        "Bạn là chuyên gia nghiên cứu người Việt. "
        "MỌI câu trả lời BẮT BUỘC dùng TIẾNG VIỆT, "
        "không dùng tiếng Anh trừ khi là thuật ngữ bắt buộc."
        "Trích dẫn nguồn đến thông tin."
    ),
    llm=gemini_llm,
    verbose=True,
)

analysis_agent = Agent(
    role="Critical Analyst",
    goal="Phân tích logic, chi tiết và phản biện bằng TIẾNG VIỆT",
    backstory=(
        "Senior analyst who challenges assumptions."
        "ALL analytical content MUST be written in VIETNAMESE."
    ),
    llm=claude_llm,
    verbose=True,
)

trend_agent = Agent(
    role="Social & Trend Analyst",
    goal=(
        "Cập nhật xu hướng mới nhất và các quan điểm trái chiều "
        "từ mạng xã hội X (Twitter) bằng TIẾNG VIỆT"
    ),
    backstory=(
        "Bạn là chuyên gia theo dõi mạng xã hội và xu hướng thời gian thực. "
        "Nhiệm vụ của bạn là tìm các insight mới, các luồng ý kiến trái chiều, "
        "và các chủ đề đang được thảo luận trên X trong vòng 6 tháng gần đây. "
        "KHÔNG lặp lại phân tích trước đó."
    ),
    llm=grok_llm,
    verbose=True,
)

content_agent = Agent(
    role="Content Strategist",
    goal="Create high-quality, structured, creative content",
    backstory=(
        "Professional Vietnamese writer for reports, blog posts, and social media content."
        "Do not use English in the output."
    ),
    llm=chatgpt_llm,
    verbose=True,
)

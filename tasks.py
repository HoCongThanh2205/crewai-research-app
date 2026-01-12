from crewai import Task
from agents import research_agent, analysis_agent,trend_agent, content_agent

research_task = Task(
    description="""
    Research the topic: "{topic}"

    Requirements:
    - Use multiple sources
    - Provide citations (URL or source name)
    - Neutral, factual tone
    """,
    expected_output="""
    A research brief with bullet points and cited sources.
    """,
    agent=research_agent,
)

analysis_task = Task(
    description="""
    Analyze the research findings.

    Requirements:
    - MUST be written in Vietnamese
    - Logical structure
    - Identify strengths, weaknesses
    - Add counter-arguments
    """,
    expected_output="""
    A structured analytical report with critiques, detailed analysis report in VIETNAMESE.
    """,
    agent=analysis_agent,
    context=[research_task],
)

trend_task = Task(
    description="""
    Dựa trên KẾT QUẢ PHÂN TÍCH của Claude ở trên,
    hãy thực hiện các nhiệm vụ sau:

    YÊU CẦU:
    - Tìm các XU HƯỚNG MỚI NHẤT trong 6 tháng gần đây
      liên quan đến chủ đề đang nghiên cứu trên mạng xã hội X (Twitter)
    - Nêu các Ý KIẾN TRÁI CHIỀU hoặc tranh luận đáng chú ý (nếu có)
    - Làm rõ:
        + Quan điểm ủng hộ
        + Quan điểm phản đối / nghi ngờ
        + Các chủ đề đang được thảo luận nhiều
    - Viết HOÀN TOÀN bằng TIẾNG VIỆT
    - KHÔNG lặp lại nội dung của research hoặc analysis
    """,
    expected_output="""
    Báo cáo xu hướng và quan điểm trái chiều từ mạng xã hội X
    trong 6 tháng gần đây, viết bằng tiếng Việt.
    """,
    agent=trend_agent,
    context=[research_task, analysis_task],
)

content_task = Task(
    description="""
    Create content from the analysis, trend.

    Deliverables:
    1. MUST be written in Vietnamese
    2. Executive summary (for decision makers)
    3. Full report
    4. Blog article
    5. 3 short social media posts
    """,
    expected_output="""
    The content is written in Vietnamese, well-formatted, and ready for publication.
    """,
    agent=content_agent,
    context=[research_task, analysis_task, trend_task],
)

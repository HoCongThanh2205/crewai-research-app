from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool

# ========= MOCK TOOLS =========

class PerplexityTool(BaseTool):
    name: str = "Perplexity Research"
    description: str = "Mock research tool like Perplexity"

    def _run(self, query: str) -> str:
        return f"""
        Research findings for: {query}

        • Study A (PMID: 12345678) shows promising results.
        • Study B (DOI: 10.1000/j.jmb.2024.01.001) confirms effectiveness.
        """

class ClaudeAnalysisTool(BaseTool):
    name: str = "Claude Analysis"
    description: str = "Mock analytical reasoning like Claude"

    def _run(self, text: str) -> str:
        return f"""
        Analysis Summary:
        - Evidence quality: Moderate–High
        - Consistency across studies: Good
        - Clinical applicability: Promising but needs RCTs
        """

# ========= INPUT (GOOGLE FORM GIẢ LẬP) =========

topic = input("📝 Google Form - Nhập chủ đề nghiên cứu: ").strip()
if not topic:
    print("❌ Không có chủ đề.")
    exit(1)

# ========= LLM (ChatGPT / Proxy) =========

llm = LLM(
    model="gpt-4o-mini",
    base_url="https://v98store.com/v1",
    api_key="sk-6TIr02rlYWdNPydYd7HifZHZriShnf9j7w2SxDMULCOsUEfI",
    temperature=0.1
)

# ========= AGENTS =========

research_agent = Agent(
    role="Research Agent",
    goal="Thu thập nghiên cứu y khoa",
    backstory="Bạn mô phỏng Perplexity AI.",
    tools=[PerplexityTool()],
    verbose=True,
    llm=llm
)

analysis_agent = Agent(
    role="Analysis Agent",
    goal="Phân tích và đánh giá chất lượng nghiên cứu",
    backstory="Bạn mô phỏng Claude AI.",
    tools=[ClaudeAnalysisTool()],
    verbose=True,
    llm=llm
)

writing_agent = Agent(
    role="Writing Agent",
    goal="Viết báo cáo tổng hợp dễ đọc",
    backstory="Bạn mô phỏng ChatGPT sáng tạo.",
    verbose=True,
    llm=llm
)

# ========= TASKS =========

task_research = Task(
    description=f"Tìm nghiên cứu về: {topic}",
    expected_output="Danh sách nghiên cứu",
    agent=research_agent
)

task_analysis = Task(
    description="Phân tích các nghiên cứu đã thu thập",
    expected_output="Đánh giá chất lượng bằng chứng",
    agent=analysis_agent
)

task_writing = Task(
    description="""
    Viết báo cáo cuối cùng cho bác sĩ:
    - Giới thiệu
    - Tóm tắt nghiên cứu
    - Phân tích
    - Kết luận
    """,
    expected_output="Báo cáo hoàn chỉnh",
    agent=writing_agent
)

# ========= CREW =========

crew = Crew(
    agents=[research_agent, analysis_agent, writing_agent],
    tasks=[task_research, task_analysis, task_writing]
)

# ========= RUN =========

print("\n🚀 BẮT ĐẦU DEMO WORKFLOW...\n")
result = crew.kickoff()

print("\n================ FINAL OUTPUT ================\n")
print(result)

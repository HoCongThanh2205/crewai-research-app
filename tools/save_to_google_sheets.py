from crewai.tools import tool
from .google_sheets_writer import write_to_google_sheets

@tool("save_to_google_sheets")
def save_to_google_sheets_tool(
    topic: str,
    research: str,
    analysis: str,
    trend: str,
    content: str
):
    """
    Lưu dữ liệu vào Google Sheets
    """
    write_to_google_sheets(topic, research, analysis, trend, content)
    return "Saved to Google Sheets"

import requests

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzFl7vPzzBE9fEuEfIq67_P0Ct2kf7rR3eSZBDdNHZd_Og8AgjX5Vbsc5ZuJhYoXAw9/exec"

def write_to_google_sheets(
    topic: str,
    research: str,
    analysis: str,
    trend: str,
    content: str,
    timeline: str = ""
):
    payload = {
        "topic": topic,
        "research": research,
        "analysis": analysis,
        "trend": trend,
        "content": content,
        "timeline": timeline,
    }

    res = requests.post(WEBHOOK_URL, json=payload, timeout=20)
    return res.status_code

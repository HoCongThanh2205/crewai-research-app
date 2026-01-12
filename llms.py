from crewai import LLM

BASE_URL = "https://v98store.com/v1"
API_KEY = "sk-6TIr02rlYWdNPydYd7HifZHZriShnf9j7w2SxDMULCOsUEfI"

COMMON = {
    "base_url": BASE_URL,
    "api_key": API_KEY,
    "provider": "openai",   # ÉP CREWAI KHÔNG AUTO-DETECT
}

# 🔍 Research (Gemini)
gemini_llm = LLM(
    model="gemini-2.5-pro",
    **COMMON
)

# 🧠 Analysis (Claude)
claude_llm = LLM(
    model="claude-3-5-sonnet-20241022",
    **COMMON
)

# Trends & Contrarian Views
grok_llm = LLM(
    model="grok-3",
    **COMMON
)

# ✍️ Content (ChatGPT)
chatgpt_llm = LLM(
    model="gpt-4o-mini",
    temperature=0.1,
    **COMMON
)

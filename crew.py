from crewai import Crew, Process
from tasks import research_task, analysis_task, trend_task, content_task
from agents import research_agent, analysis_agent, trend_agent, content_agent

def build_crew(topic: str):
    research_task.description = research_task.description.format(topic=topic)

    return Crew(
        agents=[
            research_agent,
            analysis_agent,
            trend_agent,
            content_agent,
        ],
        tasks=[
            research_task,
            analysis_task,
            trend_task,
            content_task,
        ],
        process=Process.sequential,
        language="vi",
        verbose=True,
    )

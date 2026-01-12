from dotenv import load_dotenv
load_dotenv() # load nội dung từ file .env

from crewai import Agent, Task, Crew

# 1. Tạo một Agent đơn giản
test_agent = Agent(
    role='Greeting AI',
    goal='Say hello to the user',
    backstory='You are a friendly AI assistant.',
    verbose=True
)

# 2. Tạo Task
task = Task(
    description='Say "Xin chào! CrewAI đã được cài đặt thành công!" in Vietnamese.',
    expected_output='A greeting sentence.',
    agent=test_agent
)

# 3. Chạy Crew
crew = Crew(agents=[test_agent], tasks=[task])
result = crew.kickoff()

print(result)
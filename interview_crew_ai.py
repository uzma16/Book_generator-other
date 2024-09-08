# from pymongo import MongoClient
# from datetime import datetime
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
import uuid
import os

# # MongoDB Configuration
# mongo_uri = "mongodb://localhost:27017"
# mongo_db_name = "SparkAI"
# mongo_collection_name = "Questions_Answer"

# # Setup MongoDB client and collection
# mongo_client = MongoClient(mongo_uri)
# mongo_db = mongo_client[mongo_db_name]
# questions_answer_collection = mongo_db[mongo_collection_name]

# Claude Haiku API Configuration
os.environ["ANTHROPIC_API_KEY"] = "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"

claude_llm = ChatAnthropic(
    model="claude-3-haiku-20240307"
)

llm_config = {
    "seed": 42,
    "llm": claude_llm,
    "temperature": 0
}

# # Function to save messages to MongoDB
# def save_messages_to_mongo(agent, output, config):
#     message_content = {
#         "timestamp": datetime.now(),
#         "content": output.raw_output,
#         "role": agent.role if agent.role == "User_proxy" else "interviewer"
#     }
    
#     session_id = config.get("session_id", None)
#     if session_id is None:
#         # Start new session
#         session_id = str(uuid.uuid4())  # Generate new session ID
#         interview_data = {
#             "_id": session_id,
#             "session_id": session_id,
#             "start_time": datetime.now(),
#             "messages": [message_content],
#             "status": "In Progress"
#         }
#         questions_answer_collection.insert_one(interview_data)
#         config["session_id"] = session_id  # Store session ID in the config
#     else:
#         # Update existing session
#         questions_answer_collection.update_one(
#             {"session_id": session_id},
#             {
#                 "$push": {"messages": message_content},
#                 "$set": {"end_time": datetime.now()}
#             }
#         )
    
#     # Continue the agent communication flow
#     return output


# UserProxyAgent to simulate user input
user_proxy = Agent(
    role="User_proxy",
    goal="You are now interacting with the interview system.",
    backstory="You are simulating user input for the interview system.",
    llm=claude_llm,  # Providing the same LLM, but it won't be used
    tools=[],  # Ensure an empty list for tools
    verbose=True
)

# InterviewerAgent to ask questions and process responses
interviewer = Agent(
    role="Interviewer",
    goal="""My first question would be 'Tell me the problem that you want to solve' then going forward
    I will ask another question related to user's problem only, because my work is to collect all the info about user problem by asking questions. So that 
    when my planner team works to solve the problem or plan the solution, it will have all the information given by the user. I will also ask about the timeline of completion of the problem""",
    backstory="You are responsible for conducting interviews to gather detailed information about user problems and timelines.",
    llm=claude_llm,  # Set the LLM configuration directly
    tools=[],  # Ensure an empty list for tools
    verbose=True
)

# Create tasks for the agents
user_proxy_task = Task(
    description="Initiate the interview",
    agent=user_proxy,
    expected_output="Please proceed with my interview"
)

interview_task = Task(
    description="Conduct the interview",
    agent=interviewer,
    tools=[],  # Assuming no additional tools are needed
    # callback=save_messages_to_mongo,
    # config={"session_id": None}
    expected_output="Questions to get info from user"
)

# Assemble the crew
crew = Crew(
    agents=[user_proxy, interviewer],
    tasks=[user_proxy_task, interview_task],
    verbose=True
)

# Start the chat
result = crew.kickoff()
print(result)
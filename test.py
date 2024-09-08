from textwrap import dedent
# from crewai_tools import BaseTool
from crewai import Agent, Task, Crew

import os
# os.environ['OPENAI_API_KEY'] = 'ixfie6Gk89q0kjcpkCcPvyQOXBZRMKsMrgehAzN1'
import anthropic
client = anthropic.Anthropic(
# defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="ixfie6Gk89q0kjcpkCcPvyQOXBZRMKsMrgehAzN1",
)
# class Agent():
def task_decomposer_agent():
    return Agent(
        role="Task Decomposer",
        goal=dedent("""\
            Analyze given tasks and break them down into smaller steps, manageable & doable actions that can be executed sequentially or in parallel to achieve the overall objectives efficiently."""),
        backstory=dedent("""\
            As a Task Decomposer, your expertise lies in management and process optimization. With a keen eye for detail and a methodical approach,
                        you specialize in dissecting complex tasks into their constituent parts or smaller steps, ensuring each step is clearly 
                        defined and actionable."""),
        allow_delegation=False,
        verbose=True
    )

# class Task():
def task_decomposer(agent,task):
    return Task(
        description=dedent(f"""
            Break down the given task into smaller, actionable & doable steps. 
            Task : {task}
            The agent should systematically analyze the task and outline each step necessary to efficiently complete the process from start to finish."""),
        agent=agent,
        expected_output=dedent("""
            Step-by-step actions to complete the task:
            Step 1: Open the platform using using its URL (example: if platform is linkedin then url is https://www.linkedin.com/).
            Step 2: Navigate to the posting area by clicking on the 'Start a post' area at the top of the home feed.
            Step 3: Call the API to generate the content for the post focused on 'AI'. Use parameters to specify the topic and desired length.
            Step 4: Retrieve the post content from the API and input it into the LinkedIn post editor.
            Step 6: Click the 'Post' button to publish it on given platform (ex: Linkedin).""")
    )

class Task_Crew:
    def __init__(self, task):
       self.task = task

    def run(self):
        # agents = Agent()
        # tasks = Task()

        # Initialize agents
        # task_decomposer_agent = agents.task_decomposer_agent()
        task_decomposer_a = task_decomposer_agent()


        # Define tasks
        task_decompo = task_decomposer(
            task_decomposer_a,
            task
        )

        # Create and run the crew
        crew = Crew(
            agents=[
                task_decomposer_a
            ],
            tasks=[task_decompo],
            verbose=True
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to the Task Decomposer Project")
    print('-----------------------------------------------')
    task = input(
        dedent("""
            Give the task?
        """))
    
    task_crew = Task_Crew(task)
    result = task_crew.run()
    print("\n\n########################")
    print("## Here is your Result")
    print("########################\n")
    print(result)
    
# import requests
# from textwrap import dedent
# from crewai import Agent, Task, Crew, Process

# def haikucloud_api_call(api_key, endpoint, payload):
#     """ Generic function to call HaikuCloud API """
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.post(f'https://api.haikucloud.com/{endpoint}', headers=headers, json=payload)
#     return response.json()

# class AgentUtils:
#     @staticmethod
#     def task_decomposer_agent():
#         return Agent(
#             role="Task Decomposer",
#             goal=dedent("""\
#                 Analyze given tasks and break them down into smaller steps, manageable & doable actions that can be executed sequentially or in parallel to achieve the overall objectives efficiently."""),
#             backstory=dedent("""\
#                 As a Task Decomposer, your expertise lies in management and process optimization. With a keen eye for detail and a methodical approach,
#                 you specialize in dissecting complex tasks into their constituent parts or smaller steps, ensuring each step is clearly 
#                 defined and actionable."""),
#             allow_delegation=False,
#             verbose=True
#         )

# class TaskUtils:
#     @staticmethod
#     def task_decomposer(agent, task_description, api_key):
#         # Example call to HaikuCloud to get detailed steps based on the task description
#         steps = haikucloud_api_call(api_key, 'generate-task-steps', {'task_description': task_description})
#         detailed_steps = "\n".join(f"Step {i+1}: {step}" for i, step in enumerate(steps['data']))

#         return Task(
#             description=dedent(f"""
#                 Break down the given task into smaller, actionable & doable steps.
#                 Task: {task_description}
#                 The agent should systematically analyze the task and outline each step necessary to efficiently complete the process from start to finish."""),
#             agent=agent,
#             expected_output=detailed_steps
#         )

# class TaskCrew:
#     def __init__(self, task_description, api_key):
#        self.task_description = task_description
#        self.api_key = api_key

#     def run(self):
#         task_decomposer_agent = AgentUtils.task_decomposer_agent()
#         task_decomposer = TaskUtils.task_decomposer(task_decomposer_agent, self.task_description, self.api_key)

#         crew = Crew(
#             agents=[task_decomposer_agent],
#             tasks=[task_decomposer],
#             verbose=True
#         )

#         result = crew.kickoff()
#         return result
    
# import os
# if __name__ == "__main__":
#     api_key = 'ixfie6Gk89q0kjcpkCcPvyQOXBZRMKsMrgehAzN1'  # Replace with your actual API key
#     print("## Welcome to the Task Decomposer Project")
#     task_description = input("Please provide the task description:\n")
#     # os.environ['api_key'] = 'sk-proj-lG2Fk8i7e6nt5N9fNTovT3BlbkFJ74J0EJw5Vooi5pKyMgFT'
#     # api_key="ixfie6Gk89q0kjcpkCcPvyQOXBZRMKsMrgehAzN1"
#     task_crew = TaskCrew(task_description, api_key)
#     result = task_crew.run()
#     print("\n## Here is your Result\n")
#     print(result)

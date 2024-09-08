import os
from textwrap import dedent
# from crewai_tools import BaseTool
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
# os.environ["ANTHROPIC_API_KEY"] = "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"

# from langchain_anthropic import ChatAnthropic

# ClaudeHaiku = ChatAnthropic(
#     model="claude-3-haiku-20240307"
# )


os.environ["GROQ_API_KEY"] = "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"
# os.environ["GROQ_API_BASE"] = "https://api.groq.com/openai/v1"  # Ensure this is correct

# Verify environment variables
print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))
print("GROQ_API_BASE:", os.environ.get("GROQ_API_BASE"))

def get_llm():
    llm=ChatGroq(temperature=0,
                model_name="llama3-70b-8192",
                api_key="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")
    return llm

def task_decomposer_agent():
    return Agent(
        role="Task Decomposer",
        goal=dedent("""\
            Analyze given tasks and break them down into smaller steps, manageable & doable actions that can be executed sequentially or in parallel to achieve the overall objectives efficiently."""),
        backstory=dedent("""\
            As a Task Decomposer, your expertise lies in management and process optimization. With a keen eye for detail and a methodical approach,
                        you specialize in dissecting complex tasks into their constituent parts or smaller steps, ensuring each step is clearly 
                        defined and actionable."""),
        llm=get_llm(),
        allow_delegation=False,
        verbose=True
    )

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
            Step 4: Retrieve the post content from the API and input it into the platform post editor.
            Step 6: Click the 'Post' button to publish it on given platform (ex: Linkedin).
                .
                .
            Step n: According to requirement.""")
    )

class Task_Crew:
    def __init__(self, task):
       self.task = task

    def run(self):
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
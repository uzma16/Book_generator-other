import autogen
import chromadb
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

config_list = [
    {
        "model": "gpt-4-turbo-preview",
        "api_key":"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"
    }
]

llm_config_proxy = {
    "temperature": 0,
    "config_list": config_list,
}

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config_proxy,
    system_message="""You are a helpful assistant. Provide accurate answers based on the context. Respond "Unsure about answer" if uncertain.""",
)

user = RetrieveUserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    system_message="Assistant who has extra content retrieval power for solving difficult problems.",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "code",
        "docs_path": ['autogen.pdf'],
        "chunk_token_size": 1000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path='/tmp/chromadb'),
        "collection_name": "pdfreader",
        "get_or_create": True,
    },
    code_execution_config={"work_dir": "coding","use_docker": False},
)

user_question = """
Compose a short LinkedIn post showcasing how AutoGen is revolutionizing the future of Generative AI 
through the collaboration of various agents. Craft an introduction, main body, and a compelling 
conclusion. Encourage readers to share the post. Keep the post under 500 words.
"""

user.initiate_chat(
    assistant,
    message=user_question,
)
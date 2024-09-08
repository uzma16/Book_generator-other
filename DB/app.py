import json, os, chromadb, autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.retrieve_utils import TEXT_FORMATS

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
)

# Database client setup
db_client = chromadb.PersistentClient(path="/path/to/your/chromadb")

# RetrieveAssistantAgent instance
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

# RetrieveUserProxyAgent instance with database search configuration
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": [
            # Assuming these paths are correctly indexed in your ChromaDB instance
            "path_to_document_1",
            "path_to_document_2"
        ],
        "custom_text_types": ["md"],
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": db_client,  # Use the ChromaDB client
        "embedding_model": "all-mpnet-base-v2",
        "get_or_create": True,  
    },
    code_execution_config=False
)

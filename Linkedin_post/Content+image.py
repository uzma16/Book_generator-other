import requests
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

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config_proxy,
    system_message="You are a helpful assistant. Provide accurate answers based on the context. Respond 'Unsure about answer' if uncertain.",
)

def fetch_unsplash_image(query):
    api_key = "Vq3QmyNK_3bOh_NpQehngm52DbLtuJo3L2GTGdJjY5o"  # Replace with your actual API key
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {"query": query, "page": 1, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results'][0]['urls']['regular'] if data['results'] else "No image found"
    return "Failed to retrieve images"

def handle_user_request(user_agent, assistant_agent, initial_message):
    # Step 1: Initiate chat with the assistant agent to get the text content
    text_response = user_agent.initiate_chat(assistant_agent, message=initial_message)
    
    # Assume text_response.text provides the response from the assistant
    # Extract relevant keywords or use the initial message for image search
    image_query = "Generative AI"  # You can modify this to be more dynamic based on text_response
    image_url = fetch_unsplash_image(image_query)

    return text_response, image_url

user_question = """
Compose a short LinkedIn post showcasing how AutoGen is revolutionizing the future of Generative AI 
through the collaboration of various agents. Craft an introduction, main body, and a compelling 
conclusion. Encourage readers to share the post. Keep the post under 500 words.
"""

# Handle the request and get both text and image responses
text_response, image_url = handle_user_request(user, assistant, user_question)
print("Image URL:", image_url)

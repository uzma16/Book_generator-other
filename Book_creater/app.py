import autogen
import chromadb
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

# Configuration for the LLMs
config_list = [
    {
        "model": "gpt-4-turbo-preview",
        "api_key": "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"
    }
]

# Configuring the agent with LLM specifics
llm_config_indexer = {
    "temperature": 0.5,  # Adjusted for creativity in indexing
    "config_list": config_list,
}

# Creating an AssistantAgent specialized in generating book indexes
indexer_agent = AssistantAgent(
    name="indexer",
    llm_config=llm_config_indexer,
    system_message="You are a smart indexing assistant. Generate concise and accurate book indexes. If unsure, respond with 'Needs further clarification'.",
)

# User agent to simulate book content input and receive index
book_content_agent = RetrieveUserProxyAgent(
    name="book_content",
    human_input_mode="NEVER",
    system_message="Assistant capable of processing book content to generate structured indexes.",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "content_indexing",
        "docs_path": ['book.pdf'],  # Path to the PDF file of the book
        "chunk_token_size": 500,  # Adjust based on average page length/content density
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path='/tmp/chromadb'),
        "collection_name": "pdfindexer",
        "get_or_create": True,
    },
    code_execution_config={"work_dir": "indexing", "use_docker": False},
)

writer_content_agent = RetrieveUserProxyAgent(
    name="writer",
    human_input_mode="NEVER",
    system_message="You are a creative writer. Produce detailed and informative content about provided subtopics within 200-300 words.",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "content_generation",
        "docs_path": ['repository_of_information.pdf'],  # Adjust as necessary for source documents
        "chunk_token_size": 500,  # Fine-tune based on the complexity of content needed
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path='/tmp/chromadb'),
        "collection_name": "knowledge_base",
        "get_or_create": True,
    },
    code_execution_config={"work_dir": "content_creation", "use_docker": False},
)

writer_agent = AssistantAgent(
    name="writer",
    llm_config=llm_config_indexer,  # Assuming the same LLM configuration can be used
    system_message="You are a creative writer. Produce detailed and informative content about provided subtopics within 200-300 words."
)

# Example book content to be indexed
book_content = """
Generate a comprehensive index for the book titled 'Introduction to LLM's', emphasizing key terms, chapters, and significant concepts. The index should provide a detailed overview of the book's content, facilitating easy navigation and understanding of its core themes and subject matter.
"""

# Starting the interaction with the book content
output=book_content_agent.initiate_chat(
    indexer_agent,
    message=book_content,
)
print("output=============",output)

index_content = output.summary
print("++++++++++",index_content)

import re
import sqlite3


def setup_database():
    conn = sqlite3.connect('index_database.db')
    c = conn.cursor()
    # Add a new column 'content' if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS index_topics
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, letter TEXT, main_topic TEXT, subtopic TEXT, page_range TEXT, content TEXT DEFAULT '')''')
    conn.commit()
    conn.close()


def save_topics_to_database(topics):
    conn = sqlite3.connect('index_database.db')
    c = conn.cursor()
    for topic in topics:
        c.execute("INSERT INTO index_topics (letter, main_topic, subtopic, page_range) VALUES (?, ?, ?, ?)", topic)
    conn.commit()
    conn.close()

def parse_and_save_index(output):
    index_content = output
    pattern = re.compile(r"([A-Z])\n- (.+?), (\d+-\d+)((?:\n  - .+?, \d+-\d+)*)")
    matches = pattern.findall(index_content)
    topics = []
    for letter, main_topic, page_range, subtopics in matches:
        main_topic_strip = main_topic.strip()  
        subtopics_list = [subtopic.strip() for subtopic in subtopics.split('\n  - ')] 
        topics.append((letter, main_topic_strip, "", page_range)) 
        for subtopic in subtopics_list:
            subtopic_split = subtopic.split(', ')
            if len(subtopic_split) >= 2:
                topics.append((letter, main_topic_strip, subtopic_split[0], subtopic_split[1])) 

    save_topics_to_database(topics)

setup_database()
parse_and_save_index(index_content)

def fetch_subtopics():
    conn = sqlite3.connect('index_database.db')
    c = conn.cursor()
    c.execute("SELECT id, subtopic FROM index_topics WHERE content = '' AND subtopic != ''")
    subtopics = c.fetchall()
    conn.close()
    return subtopics

def write_content_for_subtopics(subtopics):
    for subtopic_id, subtopic in subtopics:
        # content_request = f"Write a detailed and informative chapter about '{subtopic}' in 300-400 words."
        content_request = f"Compose a comprehensive and enlightening chapter focusing on '{subtopic}' within the range of 300-400 words. Delve into the intricacies, significance, and relevance of '{subtopic}' within its broader context, providing readers with a deep understanding of its implications, applications, and potential impact. Ensure clarity, coherence, and depth in your exploration, offering valuable insights and analysis to engage and enlighten readers."
        response = writer_content_agent.initiate_chat(
            writer_agent,  # Typically, no other agent is targeted in this direct interaction
            message=content_request
        )
        # content_response = response.get_response() if response and hasattr(response, 'get_response') else "No content generated"
        content_response=response.summary
        update_subtopic_content(subtopic_id, content_response)

def update_subtopic_content(subtopic_id, content):
    conn = sqlite3.connect('index_database.db')
    c = conn.cursor()
    c.execute("UPDATE index_topics SET content = ? WHERE id = ?", (content, subtopic_id))
    conn.commit()
    conn.close()

# Example usage
setup_database()
subtopics_to_write = fetch_subtopics()
print("++++++++++++++++",subtopics_to_write)
write_content_for_subtopics(subtopics_to_write)



# import re

# # Regular expression to match topics and page numbers
# pattern = re.compile(r"([A-Z])\n- (.+?), (\d+-\d+)")

# # Find all matches in the index content
# matches = pattern.findall(index_content)

# # Extract topics and page numbers
# topics = [(letter, topic, page_range) for letter, topic, page_range in matches]


# import sqlite3

# def setup_database():
#     conn = sqlite3.connect('index_database.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS index_topics
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT, letter TEXT, topic TEXT, page_range TEXT)''')
#     conn.commit()
#     conn.close()

# def save_topics_to_database(topics):
#     conn = sqlite3.connect('index_database.db')
#     c = conn.cursor()
#     for letter, topic, page_range in topics:
#         c.execute("INSERT INTO index_topics (letter, topic, page_range) VALUES (?, ?, ?)", (letter, topic, page_range))
#     conn.commit()
#     conn.close()

# # Setup the database
# setup_database()

# # Save the topics to the database
# save_topics_to_database(topics)

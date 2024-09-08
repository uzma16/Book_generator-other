import json, os, chromadb, autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
# Accepted file formats for that can be stored in a vector database instance
from autogen.retrieve_utils import TEXT_FORMATS

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
)

# 1. create an RetrieveAssistantAgent instance named "assistant"
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

# 2. create the RetrieveUserProxyAgent instance named "ragproxyagent"
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": [
            "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
            "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Research.md",
            os.path.join(os.path.abspath(""), "..", "website", "docs"),
        ],
        "custom_text_types": ["mdx"],
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "embedding_model": "all-mpnet-base-v2",
        "get_or_create": True,  
    },
    code_execution_config=False
)

# # Example 1: Generate code based off docstrings w/o human feedback

# assistant.reset()
# code_problem = "How can I use FLAML to perform a classification task and use spark to do parallel training. Train 30 seconds and force cancel jobs if time limit is reached."
# ragproxyagent.initiate_chat(
#     assistant, problem=code_problem, search_string="spark"
# )  

# #  Example 2: Answer a question based off docstrings w/o human feedback

# assistant.reset()
# qa_problem = "Who is the author of FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=qa_problem)

# # Example 3: Generate code based off docstrings w/ human feedback

# assistant.reset()
# ragproxyagent.human_input_mode = "ALWAYS"
# code_problem = "how to build a time series forecasting model for stock price using FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=code_problem)

# # Example 4: Answer a question based off docstrings w/ human feedback.

# assistant.reset()
# ragproxyagent.human_input_mode = "ALWAYS"
# qa_problem = "Is there a function named `tune_automl` in FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=qa_problem)  # type "exit" to exit the conversation

# # Example 5: Solve comprehensive QA problems with RetrieveChat's unique feature `Update Context`
# # https://ai.google.com/research/NaturalQuestions

# config_list[0]["model"] = "gpt-35-turbo"
# corpus_file = "https://huggingface.co/datasets/thinkall/NaturalQuestionsQA/resolve/main/corpus.txt"

# ragproxyagent = RetrieveUserProxyAgent(
#     name="ragproxyagent",
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=10,
#     retrieve_config={
#         "task": "qa",
#         "docs_path": corpus_file,
#         "chunk_token_size": 2000,
#         "model": config_list[0]["model"],
#         "client": chromadb.PersistentClient(path="/tmp/chromadb"),
#         "collection_name": "natural-questions",
#         "chunk_mode": "one_line",
#         "embedding_model": "all-MiniLM-L6-v2",
#         "get_or_create": True, 
#     },
# )

# # queries_file = "https://huggingface.co/datasets/thinkall/NaturalQuestionsQA/resolve/main/queries.jsonl"
# queries = """{"_id": "ce2342e1feb4e119cb273c05356b33309d38fa132a1cbeac2368a337e38419b8", "text": "what is non controlling interest on balance sheet", "metadata": {"answer": ["the portion of a subsidiary corporation 's stock that is not owned by the parent corporation"]}}
# {"_id": "3a10ff0e520530c0aa33b2c7e8d989d78a8cd5d699201fc4b13d3845010994ee", "text": "how many episodes are in chicago fire season 4", "metadata": {"answer": ["23"]}}
# {"_id": "fcdb6b11969d5d3b900806f52e3d435e615c333405a1ff8247183e8db6246040", "text": "what are bulls used for on a farm", "metadata": {"answer": ["breeding", "as work oxen", "slaughtered for meat"]}}
# {"_id": "26c3b53ec44533bbdeeccffa32e094cfea0cc2a78c9f6a6c7a008ada1ad0792e", "text": "has been honoured with the wisden leading cricketer in the world award for 2016", "metadata": {"answer": ["Virat Kohli"]}}
# {"_id": "0868d0964c719a52cbcfb116971b0152123dad908ac4e0a01bc138f16a907ab3", "text": "who carried the usa flag in opening ceremony", "metadata": {"answer": ["Erin Hamlin"]}}
# """
# queries = [json.loads(line) for line in queries.split("\n") if line]
# questions = [q["text"] for q in queries]
# answers = [q["metadata"]["answer"] for q in queries]
# print(questions)
# print(answers)

# for i in range(len(questions)):
#     print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")
#     assistant.reset()
#     qa_problem = questions[i]
#     ragproxyagent.initiate_chat(assistant, problem=qa_problem, n_results=30)
    
# # Example 6: Solve comprehensive QA problems with customized prompt and few-shot learning
# # https://github.com/Alab-NII/2wikimultihop)

# PROMPT_MULTIHOP = """You're a retrieve augmented chatbot. You answer user's questions based on your own knowledge and the context provided by the user. You must think step-by-step.
# First, please learn the following examples of context and question pairs and their corresponding answers.

# Context:
# Kurram Garhi: Kurram Garhi is a small village located near the city of Bannu, which is the part of Khyber Pakhtunkhwa province of Pakistan. Its population is approximately 35000.
# Trojkrsti: Trojkrsti is a village in Municipality of Prilep, Republic of Macedonia.
# Q: Are both Kurram Garhi and Trojkrsti located in the same country?
# A: Kurram Garhi is located in the country of Pakistan. Trojkrsti is located in the country of Republic of Macedonia. Thus, they are not in the same country. So the answer is: no.


# Context:
# Early Side of Later: Early Side of Later is the third studio album by English singer- songwriter Matt Goss. It was released on 21 June 2004 by Concept Music and reached No. 78 on the UK Albums Chart.
# What's Inside: What's Inside is the fourteenth studio album by British singer- songwriter Joan Armatrading.
# Q: Which album was released earlier, What'S Inside or Cassandra'S Dream (Album)?
# A: What's Inside was released in the year 1995. Cassandra's Dream (album) was released in the year 2008. Thus, of the two, the album to release earlier is What's Inside. So the answer is: What's Inside.


# Context:
# Maria Alexandrovna (Marie of Hesse): Maria Alexandrovna , born Princess Marie of Hesse and by Rhine (8 August 1824 – 3 June 1880) was Empress of Russia as the first wife of Emperor Alexander II.
# Grand Duke Alexei Alexandrovich of Russia: Grand Duke Alexei Alexandrovich of Russia,(Russian: Алексей Александрович; 14 January 1850 (2 January O.S.) in St. Petersburg – 14 November 1908 in Paris) was the fifth child and the fourth son of Alexander II of Russia and his first wife Maria Alexandrovna (Marie of Hesse).
# Q: What is the cause of death of Grand Duke Alexei Alexandrovich Of Russia's mother?
# A: The mother of Grand Duke Alexei Alexandrovich of Russia is Maria Alexandrovna. Maria Alexandrovna died from tuberculosis. So the answer is: tuberculosis.


# Context:
# Laughter in Hell: Laughter in Hell is a 1933 American Pre-Code drama film directed by Edward L. Cahn and starring Pat O'Brien. The film's title was typical of the sensationalistic titles of many Pre-Code films.
# Edward L. Cahn: Edward L. Cahn (February 12, 1899 – August 25, 1963) was an American film director.
# Q: When did the director of film Laughter In Hell die?
# A: The film Laughter In Hell was directed by Edward L. Cahn. Edward L. Cahn died on August 25, 1963. So the answer is: August 25, 1963.

# Second, please complete the answer by thinking step-by-step.

# Context:
# {input_context}
# Q: {input_question}
# A:
# """

# # create the RetrieveUserProxyAgent instance named "ragproxyagent"
# corpus_file = "https://huggingface.co/datasets/thinkall/2WikiMultihopQA/resolve/main/corpus.txt"

# # Create a new collection for NaturalQuestions dataset
# ragproxyagent = RetrieveUserProxyAgent(
#     name="ragproxyagent",
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=3,
#     retrieve_config={
#         "task": "qa",
#         "docs_path": corpus_file,
#         "chunk_token_size": 2000,
#         "model": config_list[0]["model"],
#         "client": chromadb.PersistentClient(path="/tmp/chromadb"),
#         "collection_name": "2wikimultihopqa",
#         "chunk_mode": "one_line",
#         "embedding_model": "all-MiniLM-L6-v2",
#         "customized_prompt": PROMPT_MULTIHOP,
#         "customized_answer_prefix": "the answer is",
#         "get_or_create": True,  
#     },
# )

# # queries_file = "https://huggingface.co/datasets/thinkall/2WikiMultihopQA/resolve/main/queries.jsonl"
# queries = """{"_id": "61a46987092f11ebbdaeac1f6bf848b6", "text": "Which film came out first, Blind Shaft or The Mask Of Fu Manchu?", "metadata": {"answer": ["The Mask Of Fu Manchu"]}}
# {"_id": "a7b9672009c311ebbdb0ac1f6bf848b6", "text": "Are North Marion High School (Oregon) and Seoul High School both located in the same country?", "metadata": {"answer": ["no"]}}
# """
# queries = [json.loads(line) for line in queries.split("\n") if line]
# questions = [q["text"] for q in queries]
# answers = [q["metadata"]["answer"] for q in queries]
# print(questions)
# print(answers)

# for i in range(len(questions)):
#     print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")

#     # reset the assistant. Always reset the assistant before starting a new conversation.
#     assistant.reset()

#     qa_problem = questions[i]
#     ragproxyagent.initiate_chat(assistant, problem=qa_problem, n_results=10)
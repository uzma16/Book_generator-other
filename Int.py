from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from django.urls import reverse, reverse_lazy
from dotenv import load_dotenv
import os
load_dotenv()
import os
from litellm import completion


class KeywordAgent(AssistantAgent):
    def __init__(self, llm_config):
        super().__init__(
            name="KeywordAgent",
            system_message="I will provide four related keywords based on the user's input.",
            llm_config=llm_config,
        )

    def handler(self, recipient, messages, sender, config):
        user_message = messages[-1]
        # Generate four related keywords (mock implementation, replace with actual logic)
        related_keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]
        
        # Send the related keywords back to the user
        keyword_message = f"Here are four related keywords: {', '.join(related_keywords)}. Please choose one."
        self.send(keyword_message, sender)

        return False, None  # required to ensure the agent communication flow continues


class InterviewAgent:
    def __init__(self) -> None:
        self.config_list = [
            {
                "model": "NotRequired",  # Loaded with LiteLLM command
                "api_key": "NotRequired",  # Not needed
                "base_url": "http://127.0.0.1:4000"  # Your LiteLLM URL
            }
        ]
        self.llm_config = {
            "config_list": self.config_list,
            "temperature": 0,
        }
    
    def user_proxy(self):
        proxy = UserProxyAgent(
            name="User_proxy",
            system_message="You are now interacting with the interview system and ask one question at a time.",
            code_execution_config={"use_docker": False},
            human_input_mode="NEVER",
            is_termination_msg=lambda message: True  # Always True
        )
        return proxy
    
    def interviewer(self):
        interviewer_agent = AssistantAgent(
            name="Interviewer",
            system_message='''I will ask one question at a time. My first question would be 'Tell me the problem that you want to solve' 
            then going forward I will ask another question related to the user's problem only, because my work is to collect all the info 
            about the user problem by asking questions. So that when my planner team works to solve the problem or plan the solution it 
            will have all the information given by the user. I will also ask about the timeline of completion of the problem''',
            llm_config=self.llm_config,
        )
        return interviewer_agent
    
    def keyword_agent(self):
        return KeywordAgent(self.llm_config)


class ResumableGroupChatManager(GroupChatManager):
    def __init__(self, groupchat, history, **kwargs):
        self._groupchat = groupchat
        self.groupchat.speaker_selection_method = "round_robin"
        if history:
            self._groupchat.messages = history

        super().__init__(self._groupchat, **kwargs)

        if history:
            self.restore_from_history(history)

    def restore_from_history(self, history) -> None:
        for message in history:
            for agent in self._groupchat.agents:
                if agent != self:
                    self.send(message, agent, request_reply=False, silent=True)


if __name__ == "__main__":
    interview_agent = InterviewAgent()

    user_proxy = interview_agent.user_proxy()
    interviewer = interview_agent.interviewer()
    keyword_agent = interview_agent.keyword_agent()

    group_chat = GroupChat(agents=[user_proxy, interviewer, keyword_agent])

    group_chat_manager = ResumableGroupChatManager(group_chat, history=[])
    group_chat_manager.start()

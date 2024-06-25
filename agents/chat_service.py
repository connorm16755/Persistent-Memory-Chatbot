from agents.memory_creation_agent import MemoryCreationAgent
from agents.memory_storage_agent import MemoryStorageAgent
from agents.memory_retrieval_agent import MemoryRetrievalAgent


class ChatService:
    def __init__(self, user):
        self.memory_creation_agent = MemoryCreationAgent(user)
        self.memory_storage_agent = MemoryStorageAgent(user)
        self.memory_retrieval_agent = MemoryRetrievalAgent(user)

    def invoke(self, question):
        memory = self.memory_creation_agent.invoke(question)
        print(memory)
        try:
            relevant_context = list(self.memory_storage_agent.invoke(memory))
        except TypeError:
            relevant_context = []
        response = self.memory_retrieval_agent.invoke(_format_context(relevant_context), question)
        return response
    
def _format_context(context):
    context_str = ""
    for c in context:
        context_str += f"{c}\n"
    return context_str
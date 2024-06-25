from agents.base_model import base_model
from prompts.memory_retrieval_prompts import memory_retrieval_prompt
from memory.user_memory import user_memory, get_db



class MemoryRetrievalAgent:
    def __init__(self, user):
        self.user = user
        self.model = base_model
        self.prompt = memory_retrieval_prompt
        self.memory = user_memory(user)
    
    '''
    def _get_context(self):
        memory = self.memory
        context = ""
        for field in memory:
            if field == "_id":
                continue
            for m in memory[field]:
                context += f"* {m}\n"
        return context
    '''
    
    def invoke(self, context, question):
        # chain = self.prompt | self.model
        # response = chain.invoke({"context": self._get_context(), "question": question}).content
        # return response
        chain = memory_retrieval_prompt | self.model
        response = chain.invoke({"context": context, "question": question, "user": self.user}).content
        return response
    

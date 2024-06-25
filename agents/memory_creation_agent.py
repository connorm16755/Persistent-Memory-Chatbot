from agents.base_model import base_model
from prompts.memory_creation_prompts import memory_creation_prompt
from prompts.memory_creation_prompts import is_question_prompt
from memory.user_memory import user_memory
import re

class MemoryCreationAgent:
    def __init__(self, user):
        self.user = user
        self.model = base_model
        self.model.temperature = 0

        self.memory: dict = user_memory(user)
    
    def invoke(self, question):
        
        chain = memory_creation_prompt | self.model
        response = eval(
            chain.invoke({
                "question": question, 
                "field_list": self._get_fields()}).content
        )
        self._clean_memory(response)
        response["_id"] = self.user
        return response
    
    def _get_fields(self):
        fields = self.memory.keys()
        field_str = ""
        for field in fields:
            field_str += f"* {field}\n"
        return field_str
    
    def _insert_name(self, text):
        new_text = re.sub('the user', self.user, text, flags=re.IGNORECASE)
        return new_text
    
    def _clean_memory(self, memory: dict[str,list]):
        for field in memory:
            mems = memory[field]
            new_mems = '$'.join(mems)
            new_mems = self._insert_name(new_mems)
            memory[field] = new_mems.split('$')


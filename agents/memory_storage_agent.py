from agents.base_model import base_model
from memory.user_memory import user_memory
from memory.user_memory import get_db

from prompts.memory_storage_prompts import identify_contradiction_prompt
from prompts.memory_storage_prompts import argument_sentiment_prompt
from prompts.memory_storage_prompts import field_similarity_prompt

import copy



class MemoryStorageAgent:
    def __init__(self, user):
        self.user = user

        self.model = base_model
        self.model.temperature = 0

        self.full_memory: dict[str, list] = user_memory(user)
        self.k = 3

    

    def invoke(self, new_memory_batch: dict):
        self._reset_memory()
        full_context = self._process_memory_batch(new_memory_batch)
        self._store_memory()
        return full_context
    
    def _reset_memory(self):
        self.full_memory = user_memory(self.user)
    
    def _process_memory_batch(self, new_memory_batch: dict):
        full_context = []
        for field in new_memory_batch:
            if field == "_id":
                self.full_memory["_id"] = new_memory_batch['_id']
                continue
            elif field == "questions":
                continue

            field_memories = new_memory_batch[field]
            for memory in field_memories:
                relevant_memories: dict = self._identify_relevant_memories(field, memory)
                context = self._remove_contradictions(field, memory, relevant_memories)
                full_context.extend([c for c in context if c not in full_context])
                self._add_to_full_memory(field, memory)
            
        if "questions" not in new_memory_batch.keys():
            return
        for question in new_memory_batch["questions"]:
            relevant_memories = self._identify_relevant_memories("questions", question)
            for field in relevant_memories:
                context = relevant_memories[field]
                full_context.extend([c for c in context if c not in full_context])
        return full_context
        


    def _add_to_full_memory(self, field, memory):
        if field in self.full_memory:
            if memory not in self.full_memory[field]:
                self.full_memory[field].append(memory)
        else:
            self.full_memory[field] = [memory]

    def _identify_relevant_memories(self, field, memory):
        relevant_fields = self._semantic_field_search(field, memory)

        relevant_memories = {}
        for field in relevant_fields:
            try:
                relevant_memories[field] = copy.deepcopy(self.full_memory[field])
            except:
                print(f"Field '{field}' does not exist. You're embarassing lololol.")

        return relevant_memories

    def _semantic_field_search(self, field, memory):
        candidate_field = field
        candidate_memory = memory

        current_fields = list(self.full_memory.keys())
        if "_id" in current_fields:
            current_fields.remove("_id")
        k = min(len(current_fields), self.k)

        relevant_fields = []
        if candidate_field in current_fields:
            relevant_fields.append(candidate_field)
            current_fields.remove(candidate_field)
            k -= 1

        current_fields_str = ""
        for cf in current_fields:
            current_fields_str += f"* {cf}\n"

        try:
            key_chain = field_similarity_prompt | self.model
            retrieved_fields = eval(key_chain.invoke({
                "field_list": current_fields_str,
                "statement": candidate_memory,
                "k": k
            }).content)
        except:
            retrieved_fields = []

        relevant_fields.extend(retrieved_fields)
        return relevant_fields
    
    def _remove_contradictions(self, field, memory, relevant_memories: dict[str,list]):
        context = []
        for rel_field in relevant_memories:
            for rel_memory in relevant_memories[rel_field]:
                contradiction_argument = self.model.invoke(identify_contradiction_prompt.format(
                    user_name = self.user,
                    statement_1=memory,
                    statement_2=rel_memory
                )).content

                sentiment_chain = argument_sentiment_prompt | self.model
                response = sentiment_chain.invoke({"argument": contradiction_argument}).content
                is_contradiction = eval(response)

                if is_contradiction:
                    try:
                        print (f"SYSTEM MESSAGE: REMOVING FROM MEMORY '{rel_memory}'")
                        self.full_memory[rel_field].remove(rel_memory)
                    except Exception as e:
                        print(f"An error occurred: {type(e).__name__}")
                        print(f"Error message: {e}")
                        print(f"OOOPS...could not remove {rel_memory}")
                elif memory not in context:
                    context.append(memory)
        return context

    

    def _store_memory(self):
            full_memory = self.full_memory
            db = get_db()
            if "_id" in full_memory:
                v = full_memory["_id"]
                db.delete_one({"_id": v})
            db.insert_one(full_memory)

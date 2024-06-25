from agents.chat_service import ChatService
from agents.memory_retrieval_agent import MemoryRetrievalAgent
from agents.memory_creation_agent import MemoryCreationAgent
from tests.performance_evaluation import performance_evaluation


chat_svc = ChatService("Connor")
while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    response = chat_svc.invoke(user_input)
    print("AI:",response)




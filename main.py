from agents.chat_service import ChatService


chat_svc = ChatService("Connor")
while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    response = chat_svc.invoke(user_input)
    print("AI:",response)

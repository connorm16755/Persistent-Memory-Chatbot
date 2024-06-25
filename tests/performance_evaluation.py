from agents.chat_service import ChatService
from time import perf_counter
from statistics import mean

'''
This performance evaluation tests

1. Knowledge Embedding: How well does the chat service store facts about the user?
2. Direct Retrieval: How well does the chat service respond to questions regarding 
    directly embedded facts?
3. Reasoning: How well does the chat service use the information it has to answer
    questions that indirectly require that knowledge?
4. Contradiction Resolution: Given contradicting information, how well does the 
    chat service update its memory and respond appropriately to direct follow-up
    questions?
5. Response Time: What is the average response time? Does it increase significantly
    as memory grows?
'''
def performance_evaluation():
    chatbot = ChatService("Connor")
    response_times = []

    knowledge_embedding = [
        "Hello, I like to learn about AI.",
        "I am a software development intern.",
        "I work at Infor.",
        "I prefer working at home than in the office.",
        "I graduate college in December.",
        "I don't like long commutes.",
        "I want to live close to where I work.",
        "I live in Atlanta.",
        "I live in an apartment.",
        "I enjoy cooking my own meals."
    ]

    for q in knowledge_embedding:
        print("You:", q)

        start = perf_counter()
        response = chatbot.invoke(q)
        end = perf_counter()

        print("AI:", response)

        response_time = end-start
        response_times.append(response_time)
        print(f"Response time: {response_time} seconds")
        print()
    
    return

    direct_retrieval = [
        "What do I like?",
        "What do I do for work?",
        "What company do I work for?",
        "Where do I prefer to work?",
        "When do I graduate college?",
        "How do I feel about long commutes?",
        "Do I want to be close or far awar from where I work?",
        "Where do I live?",
        "Do I live in an apartment or a house?",
        "Do I like to cook?"
    ]

    for q in direct_retrieval:
        print("You:", q)

        start = perf_counter()
        response = chatbot.invoke(q)
        end = perf_counter()

        print("AI:", response)

        response_time = end-start
        response_times.append(response_time)
        print(f"Response time: {response_time} seconds")
        print()

    reasoning = [
        "I am looking for a full-time job after college. What should I do for work?",
        "My new job is an hour away from where I live. What should I do?",
        "What are the best things to do in my area specifically?",
        "Do I work for a Koch subsidiary?",
        "If have time to go to a fast food restaurant or go to the grocery store, what should I do?"
    ]

    for q in reasoning:
        print("You:", q)

        start = perf_counter()
        response = chatbot.invoke(q)
        end = perf_counter()

        print("AI:", response)

        response_time = end-start
        response_times.append(response_time)
        print(f"Response time: {response_time} seconds")
        print()

    contradiction_resolution = [
        "I live in Memphis.",
        "I graduated college last spring.",
        "I don't mind long commutes. I actually enjoy driving long distances.",
        "I live in a house.",
        "I don't really like to cook."
    ]

    for q in contradiction_resolution:
        print("You:", q)

        start = perf_counter()
        response = chatbot.invoke(q)
        end = perf_counter()

        print("AI:", response)

        response_time = end-start
        response_times.append(response_time)
        print(f"Response time: {response_time} seconds")
        print()

    contradiction_follow_up = [
        "Where do I live?",
        "When do I graduate college?",
        "How do I feel about long commutes?",
        "Do I live in an apartment or a house?",
        "Do I like to cook?"
    ]

    for q in contradiction_follow_up:
        print("You:", q)

        start = perf_counter()
        response = chatbot.invoke(q)
        end = perf_counter()

        print("AI:", response)

        response_time = end-start
        response_times.append(response_time)
        print(f"Response time: {response_time} seconds")
        print()

    print("Minimum Response Time:", min(response_times), "seconds")
    print("Maximum Response Time:", max(response_times), "seconds")
    print("Average Response Time:", mean(response_times), "seconds")


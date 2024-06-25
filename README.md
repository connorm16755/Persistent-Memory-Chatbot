# Persistent Memory Chatbot
---

![Hello, I’m Connor! I am Development Intern for Infor GenAI  (9)](https://github.com/connorm16755/Persistent-Memory-Chatbot/assets/143134100/b798778f-fad8-4850-ba44-243b9aeda233)

Chatbots are found in just about every business application nowadays. Their adoption accelerated by the cultural takeover of applications like ChatGPT. Though chatbots existed before the GPT models, the swift rise of LLM technology has ushered in a new era of sophisticated chatbots. However, the new age chatbots do not come without their flaws. 

The limitations of today’s chatbots come from the underlying technology, the large language model. The input to an LLM, otherwise known as the context-window, is where users put enter their queries. Context-windows are bounded by token size, meaning they can only accept inputs that are so large before running out of space. Most prompt engineering techniques rely on saving information in the context window to improve the chances of the LLM producing a desirable output. The immediate downside of these approaches goes back to the fact that input size is limited. These techniques will work reliably only up to a certain point when they exhaust the resources the LLM has for inputs. Increasing the size of the context-window, which many of flagship models have done, seems like an intuitive solution. OpenAI reports that GPT-4 has a context window of 128K tokens, an eightfold increase over 3.5-Turbo. Problem solved, right? 

Wrong. Increasing the size of the context-window is a suboptimal solution for several reasons. For one, increasing the size of the context window incurs a quadratic penalty on the space and time complexity of model invocation. Secondly, increasing the size of the context window waters down the relative importance of information in the context window as the input grows. For large inputs, finding pertinent information in the prompt becomes a task of finding a needle in a haystack. Lastly, LLMs exhibit an unequal distribution in their attention, more easily utilizing information in the beginning and end of prompts versus the middle. 


Hence, an optimal solution would keep the context window as small as reasonably possible for speed of response and to suit the model’s attentional preferences. My solution for this problem is inspired by the MemGPT architecture. The principle behind MemGPT is allowing LLMs to manage their own context windows via tool use - selectively storing information from the context window in a persistent store or recalling it from long-term memory when appropriate. Giving LLMs a focused, yet unbounded context window. My solution aims to replicate the findings of the MemGPT research paper.![download](https://github.com/connorm16755/Persistent-Memory-Chatbot/assets/143134100/95236b9d-2912-4914-b127-11c6ecd33c2b)
  

In my solution, I use a NoSQL persistent data store to save facts about the user and the conversation history. At the time of invocation, either these memories are created and/or the user’s question is queried against the NoSQL database to retrieve relevant memories to help the LLM. 
![Screenshot 2024-06-20 135131](https://github.com/connorm16755/Persistent-Memory-Chatbot/assets/143134100/42462de8-2758-431e-a7b3-16ec033263e0)

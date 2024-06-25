import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()
base_model = AzureChatOpenAI(
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
)
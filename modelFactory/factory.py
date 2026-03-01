from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv

load_dotenv()
class ModelFactory(ABC):
    @abstractmethod
    def create_model(self,model_name:str):
        pass


class Ollama_Model_Factory(ModelFactory):
    def create_model(self,model_name:str) -> ChatOllama:
        llm_model = ChatOllama(model=model_name)
        return llm_model


class Gemini_Model_Factory(ModelFactory):
    #gemini models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-flash-lite-preview", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05", "gemini-2.5-flash-lite-preview-02-05"]
    def create_model(self,model_name:str) -> ChatGoogleGenerativeAI:
        llm_model = ChatGoogleGenerativeAI(
            model=os.getenv(model_name),
            max_output_tokens=os.getenv("TOKENS"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Add automatic retry logic with exponential backoff
        model_with_retry = llm_model.with_retry(stop_after_attempt=3) # will retry up to 3 times
        return model_with_retry
    
    
class ChatModel(ModelFactory):
    
    def createModel(self, model_name:str):
        # chatModel = init_chat_model(model_name)
        pass

# 💡 General Temperature Guidelines:
#    - Lower values (0-0.3): More deterministic, consistent responses
#    - Medium values (0.7-1.0): Balanced creativity and consistency
#    - Higher values (1.5-2.0): More creative and varied responses

# Max Tokens Parameter:
#    - The script also demonstrates the max_tokens parameter, which limits response length
#    - Lower limits (50) often result in incomplete, cut-off responses
#    - Higher limits (500) allow for complete, detailed responses
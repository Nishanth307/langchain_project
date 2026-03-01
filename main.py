from modelFactory.factory import Gemini_Model_Factory
from chat_model import ChatModel

def main():
    model = Gemini_Model_Factory().create_model("GEMINI_2.5_FLASH_MODEL")
    # response = model.invoke("Hello, how are you?")
    # print(response.content)
    ChatModel(model,"you are a helpful assitant")
    
if __name__ == "__main__":
    main()

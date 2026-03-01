from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
class ChatModel:
      model = None
      messages = []
      def __init__(self, model, system_message:str):
            self.model = model 
            if not system_message:systemMessage = "You are a helpful assistant."
            self.messages.append(
                  SystemMessage(content=system_message)
            )
            self.take_input_messages()
      
      def add_messages(self, role: str, message:str):
            if role == "user":
                  self.messages.append(HumanMessage(content=message))
            elif role == "assistant":
                  self.messages.append(AIMessage(content=message))
            elif role == "system":
                  self.messages.append(SystemMessage(content=message))
            else:
                  raise ValueError(f"Invalid role: {role}")
      
      def get_reply(self):
            try:
                  return self.model.invoke(self.messages)
            except Exception as error:
                  error_msg = str(error)
                  if "429" in error_msg:
                        print("\n💡 Rate limit hit. Try again in a few moments.")
                  elif "401" in error_msg:
                        print("\n💡 Check your API key in .env file")

      def take_input_messages(self):
            print("🤖 Hi I am a chatbot. How can I help you today?")
            while True:
                  user_input = input("👤 You: ")
                  self.add_messages("user", user_input)
                  #streaming message
                  msg = self.stream()
                  self.add_messages("assistant", msg)
                  if user_input.lower() == "exit":
                        break
                  
      def stream(self):
            response_content = ""
            print("🤖 ", end="", flush=True)
            for chunk in self.model.stream(self.messages):
                  if hasattr(chunk, "content") and chunk.content:
                        response_content += chunk.content
                        print(chunk.content, end="", flush=True)
            print("\n\n✅ Stream complete!")
            return response_content
      

# or can simply use 
#  model_name = os.getenv("AI_MODEL", "gpt-5-mini")
#  model = init_chat_model(f"azure_ai:{model_name}")
#  response = model.invoke([
#    HumanMessage(content="What is LangChain in one sentence?")
#  ])
            
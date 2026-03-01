from typing import List
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,BaseMessage
from langchain_core.prompts import ChatPromptTemplate
#for agents
class Prompting:
      def __init__(self,model):
            self.model = model
            
      def create_conversation(self, role:str,examples:List[dict], new_question:str) -> List[BaseMessage]:
            """Build message arrays programmatically."""
            messages : List[BaseMessage] = [SystemMessage(content=f"you are a {role}.")]
            
            for example in examples:
                  messages.append(HumanMessage(content=example["question"]))
                  messages.append(AIMessage(content=example["answer"]))
            
            messages.append(HumanMessage(content=new_question))
            return messages
      
      #few shot -> give some examples before answering
      def msg_prompting(self):
            emoji_messages = self.create_conversation(
                  "emoji translator",
                  [
                        {"question": "happy", "answer": "😊"},
                        {"question": "sad", "answer": "😢"},
                        {"question": "excited", "answer": "🎉"},
                  ],
                  "suprised",
            )
            print(f"Messages constructed: {len(emoji_messages)}")
            response = self.model.invoke(emoji_messages)
            print(f"AI Response: {response.content}")
            
      def template_prompting(self):
            template = ChatPromptTemplate.from_messages([
                  ("system", "You are a hepful assistant that translates {input_language} to {output_language}"),
                  ("human","{text}"),
            ])
            
            chain = template | self.model
            result =  chain.invoke({
                  "input_language": "English",
                  "output_language": "Telugu",
                  "text": "Hello, how are you?",
            })
            
            print("Telugu:", result.content)
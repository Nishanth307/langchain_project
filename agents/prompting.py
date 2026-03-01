from typing import List
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,BaseMessage
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate,FewShotChatMessagePromptTemplate
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
            
      # PromptTemplate - for simple single prompts
      def template_prompting2(self):
            simple_template = PromptTemplate.from_template(
                  "Answer this {topic} question briefly: {question}"
            )
            simple_chain = simple_template | self.model 
            result = simple_chain.invoke(
                  {"topic":"science",
                   "question":"Are trees living beings?"
                  }
            )
            print("PromptTemplate:", result.content)


      # Few-Shot Prompting with Templates
      def template_prompting3(self):
            examples = [
                  {"input": "happy", "output": "😊"},
                  {"input": "sad", "output": "😢"},
                  {"input": "excited", "output": "🎉"},
            ]
            
            example_template = ChatPromptTemplate.from_messages(
                  ("human","{input}"),
                  ("ai", "{output}"), 
            )
            
            
            few_shot_template = FewShotChatMessagePromptTemplate(
                  example_prompt=example_template,
                  examples=examples,
            )
      
            final_template = ChatPromptTemplate.from_messages([
                  ("system", "you are an emoji translator. Convert words to emojis."),
                  few_shot_template,
                  ("human","{input}")
            ])
            
            chain = final_template | self.model
            
            for word in ["angry", "love", "confused"]:
                  result = chain.invoke({"input": word})
                  print(f"{word} → {result.content}")
      #  Template Composition
      def template_prompting4(self):
            base_instructions = """You are a {role} assistant.
            Your communication style is {style}. Always be helpful and professional."""
            
            educator_template = ChatPromptTemplate.from_messages([
                  ("system", base_instructions),
                  ("system", "Focus on teaching concepts clearly with examples."),
                  ("human", "{question}"),
            ])
            
            support_template = ChatPromptTemplate.from_messages([
                  ("system", base_instructions),
                  ("system", "Focus on solving problems efficiently."),
                  ("human", "{question}"),
            ])
            
            educator_chain = educator_template | self.model
            result = educator_chain.invoke({
                  "role": "Python programming",
                  "style": "friendly and encouraging",
                  "question": "What is a list comprehension?",
            })
            print(result.content)
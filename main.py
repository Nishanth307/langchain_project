from modelFactory.factory import Gemini_Model_Factory
from agents.prompting_pydantic import PydanticPrompting

def main():
    model = Gemini_Model_Factory().create_model("GEMINI_2.5_FLASH_MODEL")
    agent = PydanticPrompting(model)
    agent.pydantic_schema()
    
if __name__ == "__main__":
    try:
        print("👋🏻 starting")
        main()
        print("🙋🏻‍♂️ finishing")
    except Exception as error:
        error_msg = str(error)
        if "429" in error_msg:
            print("\n💡 Rate limit hit. Try again in a few moments.")
        elif "401" in error_msg:
            print("\n💡 Check your API key in .env file")
        else:
            print(f"\nAn error occurred: {error_msg}")

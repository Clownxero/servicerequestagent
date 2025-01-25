import asyncio
from agent import create_agent
from config import SYSTEM_PROMPT

async def main():
    agent = create_agent()
    print("Agent initialized. Starting conversation...")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
                
            print("\nProcessing...")
            response = await agent(user_input)
            print(f"\nAssistant: {response.answer}")
            
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            
if __name__ == "__main__":
    asyncio.run(main())
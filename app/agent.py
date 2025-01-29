from openai import AsyncOpenAI
from pydantic import BaseModel
from app.config import MODEL_NAME, BASE_URL, API_KEY, SYSTEM_PROMPT
from app.tools import find_response

class Response(BaseModel):
    answer: str

class ChatMemory:
    def __init__(self):
        self.history = []
    
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 20:  # Keep the last 20 messages
            self.history.pop(0)
    
    def get_history(self):
        return self.history

def create_agent():
    client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
    memory = ChatMemory()
    
    async def run(query: str) -> Response:
        try:
            memory.add_message("user", query)
            
            # Get the response and system prompt from the database
            response_text, system_prompt = await find_response(query)
            
            messages = [
                {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
                *memory.get_history(),
            ]
            
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            memory.add_message("assistant", answer)
            
            return Response(answer=answer)
            
        except Exception as e:
            print(f"Error in agent: {str(e)}")
            return Response(answer="I apologize, but I encountered an error processing your request.")
    
    return run

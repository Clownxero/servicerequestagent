import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agent import create_agent
from app.config import MODEL_NAME, SYSTEM_PROMPT

# Load environment variables
load_dotenv(dotenv_path="../.env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service Request Agent")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Pydantic model for chat message
class ChatMessage(BaseModel):
    message: str

# Initialize the agent
try:
    agent = create_agent()
    logger.info("Agent successfully initialized")
except Exception as e:
    logger.error(f"Agent initialization failed: {str(e)}")
    agent = None

@app.get("/")
async def get():
    return FileResponse('../static/index.html')

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "model_name": MODEL_NAME
    }

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        response = await agent(chat_message.message)
        return {"response": response.answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

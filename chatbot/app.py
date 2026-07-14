"""FastAPI application for VetCare chatbot."""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from .llm import VetCareLLM
from ..mcp_server.tools import TOOLS

load_dotenv()

app = FastAPI(title="VetCare Chatbot", description="AI-powered chatbot for Meadow Vet Care")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize LLM
llm = VetCareLLM()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str = "success"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """Handle chat messages."""
    try:
        response = llm.chat(chat_request.message, TOOLS)
        return ChatResponse(response=response, status="success")
    except Exception as e:
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            status="error"
        )


@app.post("/api/reset")
async def reset_conversation():
    """Reset the conversation history."""
    llm.reset_conversation()
    return {"status": "success", "message": "Conversation reset"}


@app.get("/api/tools")
async def get_tools():
    """Get list of available tools."""
    tool_info = [
        {
            "name": tool["name"],
            "description": tool["description"]
        }
        for tool in TOOLS
    ]
    return {"tools": tool_info}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "VetCare Chatbot"}

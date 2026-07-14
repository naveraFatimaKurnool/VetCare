"""Main entry point for VetCare Chatbot."""

import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()


def main():
    """Run the VetCare Chatbot server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting VetCare Chatbot server on {host}:{port}")
    print("Open your browser and navigate to: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "chatbot.app:app",
        host=host,
        port=port,
        reload=True
    )


if __name__ == "__main__":
    main()

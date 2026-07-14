"""LLM integration for VetCare chatbot using OpenAI."""

import json
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, BOOKING_PROMPT, FALLBACK_PROMPT

load_dotenv()


class VetCareLLM:
    """LLM integration for VetCare chatbot."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        self.conversation_history: List[Dict[str, str]] = []
        self._initialize_system_prompt()

    def _initialize_system_prompt(self):
        """Initialize the conversation with system prompt."""
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def chat(self, user_message: str, tools: List[Dict[str, Any]]) -> str:
        """
        Process user message and return response.
        
        Args:
            user_message: The user's message
            tools: List of available MCP tools
            
        Returns:
            Response from the LLM
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            # Format tools for OpenAI
            formatted_tools = self._format_tools(tools)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=formatted_tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls
            if assistant_message.tool_calls:
                return self._handle_tool_calls(assistant_message, tools)
            
            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content
            })
            
            return assistant_message.content
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}. {FALLBACK_PROMPT}"
            return error_msg

    def _format_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format tools for OpenAI API."""
        formatted = []
        for tool in tools:
            formatted_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            }
            formatted.append(formatted_tool)
        return formatted

    def _handle_tool_calls(self, assistant_message, tools: List[Dict[str, Any]]) -> str:
        """Handle tool calls from the LLM."""
        # Add assistant message with tool calls to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in assistant_message.tool_calls
            ]
        })
        
        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            # Find and execute the tool
            tool_result = self._execute_tool(tool_name, tool_args, tools)
            
            # Add tool result to history
            self.conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        
        # Get final response after tool execution
        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=1000
        )
        
        final_message = final_response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": final_message
        })
        
        return final_message

    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any], tools: List[Dict[str, Any]]) -> str:
        """Execute a tool and return the result."""
        for tool in tools:
            if tool["name"] == tool_name:
                try:
                    function = tool["function"]
                    result = function(**tool_args)
                    return result
                except Exception as e:
                    return json.dumps({"error": str(e)})
        
        return json.dumps({"error": f"Tool '{tool_name}' not found"})

    def reset_conversation(self):
        """Reset the conversation history."""
        self._initialize_system_prompt()

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()

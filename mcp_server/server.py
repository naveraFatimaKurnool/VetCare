"""MCP Server for VetCare chatbot."""

from mcp.server.fastmcp import FastMCP
from .tools import TOOLS

# Create the MCP server instance
mcp = FastMCP(
    "VetCare MCP Server",
    description="MCP server for Meadow Vet Care - provides tools to query veterinary services"
)


# Register all tools
def register_tools():
    """Register all tools with the MCP server."""
    for tool in TOOLS:
        mcp.tool()(tool["function"])


# Register tools when module is imported
register_tools()


def get_tool_info():
    """Get information about all available tools."""
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"]
        }
        for tool in TOOLS
    ]


if __name__ == "__main__":
    mcp.run()

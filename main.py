# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", host='127.0.0.1', port=8050)
# mcp = FastMCP("Test")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
# Add an addition tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """subtract two numbers"""
    return a - b


# Add a dynamic greeting resource
@mcp.tool()
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="sse")
    # mcp.run()

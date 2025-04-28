import asyncio 
import json
import os
from contextlib import AsyncExitStack
from typing import Any, Dict, List
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
load_dotenv()
os.environ['groq_api_key'] = os.getenv("GROQ_API_KEY")

# Config file path - change this to your config file
# config_file = "AddTwoNums.json"
config_file = "Playwrite.json"



async def main():
    
     # Connect to the server using SSE
    async with sse_client("http://localhost:8931/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

    print("Initializing chat...")

        # Create MCP client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen-qwq-32b")
    # Create agent with memory_enabled=True
    agent = MCPAgent(
            llm=llm,
            client=client,
            max_steps=15,
            memory_enabled=True,  # Enable built-in conversation memory
        )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")


    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())





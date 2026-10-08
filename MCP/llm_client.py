import asyncio
import os

from dotenv import load_dotenv

from mcp import Client, StdioServerParameters

from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool


load_dotenv()

 
async def main():
    #Start MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with Client(server_params) as mcp_client:

        #Discover MCP tools
        mcp_tools = await mcp_client.list_tools()

        print("MCP tools discovered:\n")

        for tool in mcp_tools.tools:
            print("-", tool.name)

        langchain_tools = []

        for mcp_tool in mcp_tools.tools:

            async def call_mcp_tool(
                arguments,
                tool_name=mcp_tool.name,
            ):
                result = await mcp_client.call_tool(
                    tool_name,
                    arguments,
                )
                return result.structured_content
            
            tool = StructuredTool.from_function(
                coroutine=call_mcp_tool,
                name=mcp_tool.name,
                description=mcp_tool.description or "",
            )

            langchain_tools.append(tool)


        user_request = input("\nEnter your request: ")

        response = await llm_with_tools.ainvoke(
            user_request
        )

        print("\nLLM response:")
        print(response)

        print("\nTool calls:")
        print(response.tool_calls)

 
if __name__ == "__main__":
    asyncio.run(main())

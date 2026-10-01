import asyncio
import json
import os

from dotenv import load_dotenv
from groq import Groq

from mcp import Client, StdioServerParameters

from asyncio import tools


load_dotenv()

llm = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with Client(server_params) as mcp_client:

        # --------------------------------
        # 1. Discover MCP tools
        # --------------------------------

        mcp_tools = await mcp_client.list_tools()

        print("MCP tools:")

        for tool in mcp_tools.tools:
            print("-", tool.name)

        # --------------------------------
        # 2. Convert MCP tools to LLM tools
        # --------------------------------

        llm_tools = []

        for tool in tools.tools:
            llm_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                }
            })

        # --------------------------------
        # 3. User request
        # --------------------------------

        user_message = input("You: ")

        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]

        # --------------------------------
        # 4. Ask LLM
        # --------------------------------

        response = llm.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=llm_tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # --------------------------------
        # 5. Check whether LLM requested tool
        # --------------------------------

        if assistant_message.tool_calls:

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments,
                            }
                        }
                        for call in assistant_message.tool_calls
                    ]
                }
            )

            # --------------------------------
            # 6. Execute MCP tool
            # --------------------------------

            for call in assistant_message.tool_calls:

                tool_name = call.function.name

                arguments = json.loads(
                    call.function.arguments
                )

                print(
                    f"\nCalling MCP tool: {tool_name}"
                )

                result = await mcp_client.call_tool(
                    tool_name,
                    arguments,
                )

                # --------------------------------
                # 7. Send MCP result to LLM
                # --------------------------------

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(
                            result.structured_content
                        ),
                    }
                )

            # --------------------------------
            # 8. Ask LLM for final response
            # --------------------------------

            final_response = llm.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
            )

            print(
                "\nAssistant:",
                final_response.choices[0].message.content
            )

        else:

            print(
                "\nAssistant:",
                assistant_message.content
            )


asyncio.run(main())
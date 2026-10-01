import asyncio

from mcp import Client, StdioServerParameters


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with Client(server_params) as client:

        tools = await client.list_tools()

        print("Available tools:\n")

        for tool in tools.tools:
            print("Name:", tool.name)
            print("Description:", tool.description)
            print("Input schema:", tool.input_schema)
            print()

        result = await client.call_tool(
            "multiply",
            {
                "a": 10,
                "b": 20,
            },
        )

        print("Result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
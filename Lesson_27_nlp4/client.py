import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_hw = StdioServerParameters(command="python", args=["weather_server_hw.py"])

async def check():
    async with stdio_client(server_hw) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Discovered tools:", [t.name for t in tools.tools])  # expect BOTH now

            result = await session.call_tool(
                "get_air_quality",
                arguments={"city": "Kyiv"}
            )

            print("Air Quality in Kyiv:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(check())

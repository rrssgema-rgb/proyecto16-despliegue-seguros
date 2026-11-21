import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://proyecto16-despliegue-seguros.onrender.com/mcp"

async def main():
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("\n--- HERRAMIENTAS DISPONIBLES ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\n--- CONSULTA DE POLIZA AUTO-1001 ---")
            result = await session.call_tool(
                "consultar_cobertura",
                {"numero_poliza": "AUTO-1001"}
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            if result.is_error:
                print("La herramienta ha devuelto un error.")

asyncio.run(main())

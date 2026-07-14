from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

MCP_URL = "http://127.0.0.1:8000/mcp/"   # barra final obligatoria

mcp_client = MCPClient(lambda: streamablehttp_client(MCP_URL))
model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")

with mcp_client:
    # 1) Descubrir las tools que expone tu server MCP
    tools = mcp_client.list_tools_sync()

    # 2) Crear el agente con esas tools
    agente = Agent(
        model=model,
        system_prompt="Eres un asistente que usa las herramientas del servidor MCP.",
        tools=tools,
    )

    # 3) IMPORTANTE: todo lo que invoque tools MCP debe ocurrir DENTRO del with
    print(agente("¿Qué clima hace en Lima?"))
    print(agente("Crea el archivo /tmp/hola.txt"))

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
import json

MCP_URL = "http://127.0.0.1:8000/mcp/"   # barra final obligatoria

mcp_client = MCPClient(lambda: streamablehttp_client(MCP_URL))
model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")

with mcp_client:
    tools = mcp_client.list_tools_sync()

    # (opcional) descubrir qué resources expone el server
    res = mcp_client.list_resources_sync()
    for r in res.resources:
        print(r.uri, "|", r.name, "|", r.mimeType)

    # leer resources concretos
    greeting = mcp_client.read_resource_sync("resource://greeting")
    saludo = greeting.contents[0].text                 # "¡Hola, mundo desde el MCP!"

    users = mcp_client.read_resource_sync("data://users")
    usuarios = json.loads(users.contents[0].text)      # ["Juan", "Maria", "Pedro", "Anya"]

    system_prompt = f"""Eres un asistente.
Saludo configurado: {saludo}
Usuarios activos del sistema: {', '.join(usuarios)}
"""

    agente = Agent(model=model, tools=tools, system_prompt=system_prompt)
    print(agente("¿Quiénes son los usuarios activos?"))

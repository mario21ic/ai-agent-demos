from mcp import stdio_client, StdioServerParameters

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

# El cliente arranca main.py como subproceso y habla por stdio
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="/Users/mario21ic/miniforge3/envs/agent-aws-serverless/bin/python",
        args=["/Users/mario21ic/repo/agent-demos/strands/module2/mcp-example/main.py"],
        # env={"MCP_TRANSPORT": "stdio"},  # opcional; stdio ya es el default
    )
))
model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")

with mcp_client:
    # 1) Descubrir las tools que expone tu server MCP
    tools = mcp_client.list_tools_sync()

    # 2) Crear el agente con esas tools
    agente = Agent(
        model = model,
        system_prompt = "Eres un asistente que usa las herramientas del servidor MCP.",
        tools = tools,
    )

    # 3) IMPORTANTE: todo lo que invoque tools MCP debe ocurrir DENTRO del with
    print(agente("¿Qué clima hace en Lima?"))
    print(agente("Crea el archivo /tmp/hola.txt"))

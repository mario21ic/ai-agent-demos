# leer_resources.py
import json
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")

mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="/Users/mario21ic/miniforge3/envs/agent-aws-serverless/bin/python",
        args=["/Users/mario21ic/repo/agent-demos/strands/module2/mcp-example/main.py"],
    )
))

with mcp_client:
    # --- PASO 1: descubrir qué tools existen ---
    tools = mcp_client.list_tools_sync()
    print(f"El server expone {len(tools)} tools:\n")
    for t in tools:
        spec = t.tool_spec
        nombre = spec["name"]
        desc = spec.get("description", "(sin descripción)")

        # los parámetros están en el JSON Schema de entrada
        schema = spec.get("inputSchema", {})
        # Strands suele envolverlo como {"json": {...}}; contempla ambos casos
        json_schema = schema.get("json", schema)
        props = json_schema.get("properties", {})
        requeridos = set(json_schema.get("required", []))

        print(f"🔧 {nombre}")
        print(f"   {desc.strip().splitlines()[0]}")
        if props:
            print("   parámetros:")
            for pname, pinfo in props.items():
                tipo = pinfo.get("type", "?")
                marca = " (requerido)" if pname in requeridos else ""
                print(f"     - {pname}: {tipo}{marca}")
        print()

    # --- PASO 2: descubrir qué resources existen ---
    listado = mcp_client.list_resources_sync()
    print("Resources disponibles:")
    for r in listado.resources:
        print(f"  uri={r.uri}  name={r.name}  mime={r.mimeType}")

    # --- PASO 3: leer uno por su URI ---
    resultado = mcp_client.read_resource_sync("resource://greeting")

    print("\n── Estructura cruda que devuelve read_resource_sync ──")
    print(resultado)
    # ReadResourceResult(
    #   contents=[
    #     TextResourceContents(uri='resource://greeting',
    #                          mimeType='text/plain',
    #                          text='¡Hola, mundo desde el MCP!')
    #   ]
    # )

    # El valor útil está en .contents[0].text
    saludo = resultado.contents[0].text
    print("\nsaludo =", saludo)          # ¡Hola, mundo desde el MCP!

    users = mcp_client.read_resource_sync("data://users")
    usuarios = json.loads(users.contents[0].text)      # ["Juan", "Maria", "Pedro", "Anya"]

    system_prompt = f"""Eres un asistente.
Saludo configurado: {saludo}
Usuarios activos del sistema: {', '.join(usuarios)}
"""
    agente = Agent(model=model, tools=tools, system_prompt=system_prompt)
    print(agente("¿Quiénes son los usuarios activos?"))
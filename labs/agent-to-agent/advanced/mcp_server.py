"""
Servidor MCP (Model Context Protocol) básico.

Expone herramientas de datos financieros simulados vía streamable-HTTP en
http://127.0.0.1:8000/mcp. Cualquier cliente MCP puede descubrirlas y
usarlas -en este ejemplo, el Agente Investigador (agente_investigador.py).

Nota conceptual del ejemplo:
  - MCP (Anthropic) estandariza la comunicación agente <-> herramienta.
  - A2A (Google) estandariza la comunicación agente <-> agente.
  Son protocolos complementarios: un mismo agente puede ser cliente MCP
  (para obtener herramientas) y, al mismo tiempo, servidor A2A (para que
  otros agentes lo descubran y le deleguen tareas).
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datos Financieros")

# Datos simulados en memoria: en un caso real esto llamaría a una API externa,
# una base de datos, etc.
_PRECIOS_USD = {
    "AMZN": 231.45,
    "GOOGL": 198.72,
    "MSFT": 512.30,
}

_NOTICIAS = {
    "AMZN": [
        "Amazon anuncia expansión de su red logística en Latinoamérica.",
        "AWS reporta crecimiento de doble dígito en su último trimestre.",
    ],
    "GOOGL": [
        "Google presenta nuevas funciones de IA en su buscador.",
    ],
    "MSFT": [
        "Microsoft integra Copilot en más productos de Office.",
    ],
}


@mcp.tool()
def consultar_precio_accion(simbolo: str) -> dict:
    """Devuelve el precio actual (simulado, en USD) de una acción por su símbolo bursátil."""
    simbolo = simbolo.upper().strip()
    if simbolo not in _PRECIOS_USD:
        return {"error": f"Símbolo '{simbolo}' no encontrado"}
    return {"simbolo": simbolo, "precio_usd": _PRECIOS_USD[simbolo]}


@mcp.tool()
def consultar_noticias_empresa(simbolo: str) -> dict:
    """Devuelve titulares recientes (simulados) relacionados a una empresa por su símbolo bursátil."""
    simbolo = simbolo.upper().strip()
    return {"simbolo": simbolo, "titulares": _NOTICIAS.get(simbolo, [])}


if __name__ == "__main__":
    print("Servidor MCP 'Datos Financieros' escuchando en http://127.0.0.1:8000/mcp")
    mcp.run(transport="streamable-http")

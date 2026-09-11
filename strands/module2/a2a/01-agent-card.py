"""
Google A2A Protocol - Agent Card
=================================
Ejemplo 1: Crear un AgentCard que describe las capacidades de un agente
El AgentCard es un archivo JSON (/.well-known/agent.json) que sirve como
"tarjeta de presentación" del agente en el protocolo A2A.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ActionParameter:
    """Parámetro de entrada para una acción"""
    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class Action:
    """Una acción que el agente puede realizar"""
    id: str
    name: str
    description: str
    parameters: List[ActionParameter]


@dataclass
class AgentCard:
    """
    AgentCard del protocolo A2A de Google.
    Se sirve desde /.well-known/agent.json
    """
    name: str
    description: str
    version: str
    contact: str
    url: str
    actions: List[Action]
    authentication: Dict[str, Any]

    def to_json(self) -> str:
        """Convierte el AgentCard a JSON"""
        data = asdict(self)
        # Convertir objetos anidados a diccionarios
        data['actions'] = [
            {
                'id': action['id'],
                'name': action['name'],
                'description': action['description'],
                'parameters': [asdict(p) for p in action['parameters']]
            }
            for action in self.actions
        ]
        return json.dumps(data, indent=2)


def create_weather_agent_card() -> AgentCard:
    """Crea un AgentCard para un agente meteorológico"""

    weather_action = Action(
        id="get_weather",
        name="Get Weather",
        description="Obtiene el pronóstico del clima para una ciudad",
        parameters=[
            ActionParameter(
                name="city",
                type="string",
                description="Nombre de la ciudad",
                required=True
            ),
            ActionParameter(
                name="units",
                type="string",
                description="Unidades de temperatura (celsius/fahrenheit)",
                required=False
            )
        ]
    )

    card = AgentCard(
        name="Weather Agent",
        description="Agente que proporciona información meteorológica en tiempo real",
        version="1.0.0",
        contact="weather@example.com",
        url="https://weather-agent.example.com",
        actions=[weather_action],
        authentication={
            "type": "oauth2",
            "provider": "https://auth.example.com",
            "scopes": ["weather.read"]
        }
    )

    return card


def create_search_agent_card() -> AgentCard:
    """Crea un AgentCard para un agente de búsqueda"""

    search_action = Action(
        id="search_web",
        name="Search Web",
        description="Busca información en la web",
        parameters=[
            ActionParameter(
                name="query",
                type="string",
                description="Término de búsqueda",
                required=True
            ),
            ActionParameter(
                name="max_results",
                type="integer",
                description="Número máximo de resultados",
                required=False
            )
        ]
    )

    activities_action = Action(
        id="get_activities",
        name="Get Activities",
        description="Obtiene actividades recomendadas para un destino",
        parameters=[
            ActionParameter(
                name="destination",
                type="string",
                description="Destino/ciudad",
                required=True
            ),
            ActionParameter(
                name="weather",
                type="string",
                description="Condiciones climáticas actuales",
                required=False
            )
        ]
    )

    card = AgentCard(
        name="Search & Activities Agent",
        description="Agente que busca información y recomienda actividades",
        version="1.0.0",
        contact="search@example.com",
        url="https://search-agent.example.com",
        actions=[search_action, activities_action],
        authentication={
            "type": "oauth2",
            "provider": "https://auth.example.com",
            "scopes": ["search.read", "activities.read"]
        }
    )

    return card


def main():
    """Genera y muestra AgentCards de ejemplo"""

    print("\n" + "="*70)
    print("GOOGLE A2A PROTOCOL - AGENT CARDS")
    print("="*70 + "\n")

    # Weather Agent Card
    print("📋 WEATHER AGENT CARD")
    print("-" * 70)
    weather_card = create_weather_agent_card()
    print(weather_card.to_json())

    # Search Agent Card
    print("\n\n📋 SEARCH & ACTIVITIES AGENT CARD")
    print("-" * 70)
    search_card = create_search_agent_card()
    print(search_card.to_json())

    # Explicación
    print("\n\n📚 EXPLICACIÓN")
    print("-" * 70)
    print("""
El AgentCard es un documento JSON que describe:

1. **Identidad del Agente**:
   - name: Nombre del agente
   - description: Qué hace
   - version: Versión del API

2. **Acciones Disponibles**:
   - id: Identificador único de la acción
   - parameters: Entrada requerida con tipos de datos
   - description: Qué hace la acción

3. **Autenticación**:
   - type: Método de autenticación (OAuth2, JWT, etc.)
   - provider: Servicio de autenticación
   - scopes: Permisos requeridos

4. **Contacto y URL**:
   - contact: Email de contacto
   - url: Endpoint del agente

El AgentCard se sirve desde: https://tu-agente.com/.well-known/agent.json

Otros agentes pueden descubrir tus capacidades visitando esta URL.
    """)


if __name__ == "__main__":
    main()

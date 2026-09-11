"""
Google A2A Protocol - A2A Client
=================================
Ejemplo 3: Cliente que descubre y se comunica con múltiples agentes A2A
"""

import requests
import json
from typing import Dict, List, Any
from strands import Agent
import uuid


class A2AClient:
    """Cliente del protocolo A2A de Google"""

    def __init__(self):
        self.discovered_agents: Dict[str, Dict] = {}
        self.request_log = []

        # Agente coordinador
        self.coordinator = Agent(
            system_prompt="""Eres un coordinador de agentes. Tu trabajo es:
            1. Descubrir qué agentes están disponibles
            2. Decidir cuál agente es mejor para cada tarea
            3. Coordinar comunicación entre múltiples agentes
            Siempre responde de forma estructurada."""
        )

    def discover_agent(self, agent_url: str) -> bool:
        """
        Descubre un agente mediante su AgentCard
        (en protocolo A2A: GET /.well-known/agent.json)
        """
        try:
            url = f"{agent_url}/.well-known/agent.json"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                agent_card = response.json()
                self.discovered_agents[agent_url] = agent_card

                print(f"✓ Descubierto: {agent_card.get('name', 'Unknown Agent')}")
                print(f"  URL: {agent_url}")
                print(f"  Acciones: {len(agent_card.get('actions', []))}")

                # Mostrar acciones disponibles
                for action in agent_card.get('actions', []):
                    print(f"    - {action.get('name')}: {action.get('description')}")

                return True
            else:
                print(f"✗ Fallo al descubrir {agent_url}: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error descubriendo {agent_url}: {str(e)}")
            return False

    def call_agent_action(self, agent_url: str, action_id: str, **input_params) -> Dict[str, Any]:
        """
        Llama una acción específica en un agente remoto
        Sigue el protocolo A2A con mensaje JSON estructurado
        """
        try:
            # Construir URL del endpoint de la acción
            endpoint = f"{agent_url}/v1/actions/{action_id}"

            # Mensaje A2A
            request_payload = {
                "id": str(uuid.uuid4()),
                "action": action_id,
                "input": input_params,
                "timestamp": json.dumps(None, default=str)  # Timestamp
            }

            print(f"\n📤 Enviando tarea a {agent_url}")
            print(f"   Acción: {action_id}")
            print(f"   Parámetros: {input_params}")

            # Enviar solicitud
            response = requests.post(
                endpoint,
                json=request_payload,
                timeout=10
            )

            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✓ Respuesta recibida")
                self.request_log.append({
                    "agent": agent_url,
                    "action": action_id,
                    "request": request_payload,
                    "response": result
                })
                return result
            else:
                print(f"✗ Error: {response.status_code}")
                return {"status": "error", "code": response.status_code}

        except Exception as e:
            print(f"✗ Error llamando {agent_url}: {str(e)}")
            return {"status": "error", "error": str(e)}

    def orchestrate_travel_plan(self, destination: str):
        """
        Ejemplo de orquestación: coordina múltiples agentes
        para crear un plan de viaje
        """
        print(f"\n{'='*70}")
        print(f"🗺️  PLANIFICACIÓN DE VIAJE: {destination}")
        print(f"{'='*70}\n")

        # El coordinador decide qué agentes usar
        coordination_prompt = f"""
        Estamos planificando un viaje a {destination}.
        Necesitamos:
        1. Información del clima
        2. Actividades recomendadas
        3. Información turística

        Explica qué agentes usarías y en qué orden.
        """

        strategy = self.coordinator(coordination_prompt)
        print(f"📋 Estrategia de orquestación:\n{strategy}\n")

        # Simular llamadas a agentes
        print("Ejecutando plan de coordinación...\n")

        # Nota: En producción, estos serían agentes reales
        print("(En un escenario real, aquí se llamarían a agentes reales via A2A)")

    def print_discovery_summary(self):
        """Resumen de agentes descubiertos"""
        print(f"\n{'='*70}")
        print("AGENTES DESCUBIERTOS")
        print(f"{'='*70}\n")

        if not self.discovered_agents:
            print("No hay agentes descubiertos")
            return

        for url, card in self.discovered_agents.items():
            print(f"🤖 {card.get('name')}")
            print(f"   URL: {url}")
            print(f"   Descripción: {card.get('description')}")
            print(f"   Versión: {card.get('version')}")
            print(f"   Acciones disponibles:")
            for action in card.get('actions', []):
                print(f"     • {action.get('id')}: {action.get('name')}")
            print()

    def print_request_log(self):
        """Muestra registro de solicitudes"""
        if not self.request_log:
            return

        print(f"\n{'='*70}")
        print("REGISTRO DE SOLICITUDES A2A")
        print(f"{'='*70}\n")

        for i, log in enumerate(self.request_log, 1):
            print(f"{i}. Agente: {log['agent']}")
            print(f"   Acción: {log['action']}")
            print(f"   Estado: {log['response'].get('status', 'unknown')}")
            print()


def main():
    """Demo del cliente A2A"""

    print("\n" + "="*70)
    print("A2A CLIENT - CLIENTE DEL PROTOCOLO A2A DE GOOGLE")
    print("="*70 + "\n")

    client = A2AClient()

    print("📡 DESCUBRIMIENTO DE AGENTES")
    print("-" * 70)
    print("Intentando descubrir agentes A2A...\n")

    # Intentar descubrir agentes locales (ejemplos)
    agents_to_discover = [
        "http://localhost:5000",  # Weather Agent
        "http://localhost:5001",  # Search Agent (si está disponible)
    ]

    for agent_url in agents_to_discover:
        client.discover_agent(agent_url)

    # Mostrar resumen
    client.print_discovery_summary()

    # Ejemplo de orquestación
    print("\n📋 EJEMPLO DE ORQUESTACIÓN")
    print("-" * 70)
    client.orchestrate_travel_plan("París")

    # Instrucciones
    print("\n" + "="*70)
    print("PRÓXIMOS PASOS")
    print("="*70)
    print("""
Para probar completamente el cliente A2A:

1. Inicia el servidor A2A:
   python 02-a2a-server.py

2. En otra terminal, ejecuta el cliente:
   python 03-a2a-client.py

3. El cliente descubrirá el servidor y podrá:
   - Leer su AgentCard
   - Llamar sus acciones
   - Coordinar múltiples agentes

Protocolo A2A de Google:
- Descubrimiento: /.well-known/agent.json
- API: /v1/actions/{action_id}
- Mensaje estándar con id, action, input
- Autenticación: OAuth2 / JWT
    """)


if __name__ == "__main__":
    main()

"""
Google A2A Protocol - Complete Example
=======================================
Ejemplo 4: Ejemplo completo con autenticación JWT y comunicación A2A
Simula un Travel Planner que orquesta múltiples agentes
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any
from strands import Agent
import json
from datetime import datetime, timedelta
import jwt
import uuid


# ============================================================================
# PARTE 1: INFRAESTRUCTURA DE AUTENTICACIÓN A2A
# ============================================================================

class A2AAuthenticator:
    """Gestor de autenticación JWT para protocolo A2A"""

    def __init__(self, secret_key: str = "a2a-secret-key-dev"):
        self.secret_key = secret_key

    def create_token(self, agent_id: str, scope: List[str]) -> str:
        """Crea un token JWT para un agente"""
        payload = {
            "agent_id": agent_id,
            "scope": scope,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "error": str(e)}


# ============================================================================
# PARTE 2: MODELOS A2A
# ============================================================================

@dataclass
class A2ARequest:
    """Formato estándar de solicitud A2A"""
    id: str
    action: str
    input: Dict[str, Any]
    authorization: str = None  # Bearer token
    timestamp: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "input": self.input,
            "authorization": self.authorization,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }


@dataclass
class A2AResponse:
    """Formato estándar de respuesta A2A"""
    id: str
    action: str
    status: str  # success, error
    output: Dict[str, Any] = None
    error: str = None
    timestamp: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }


# ============================================================================
# PARTE 3: AGENTES ESPECIALIZADOS (A2A PROVIDERS)
# ============================================================================

class WeatherAgentA2A:
    """Agente de clima que implementa protocolo A2A"""

    def __init__(self):
        self.agent = Agent(
            system_prompt="""Eres un experto en meteorología. Proporciona información
            del clima de forma clara y estructurada."""
        )
        self.agent_id = "weather-agent"

    @property
    def agent_card(self) -> Dict:
        return {
            "name": "Weather Agent",
            "description": "Proporciona información meteorológica",
            "agent_id": self.agent_id,
            "version": "1.0.0",
            "actions": [
                {
                    "id": "get_weather",
                    "name": "Get Weather",
                    "description": "Obtiene clima para una ciudad",
                    "parameters": [
                        {
                            "name": "city",
                            "type": "string",
                            "required": True
                        }
                    ]
                }
            ]
        }

    def handle_action(self, request: A2ARequest) -> A2AResponse:
        """Procesa una acción A2A"""
        if request.action != "get_weather":
            return A2AResponse(
                id=request.id,
                action=request.action,
                status="error",
                error="Acción no soportada"
            )

        city = request.input.get("city")
        if not city:
            return A2AResponse(
                id=request.id,
                action=request.action,
                status="error",
                error="Parámetro 'city' requerido"
            )

        # Usar agente Strands
        response = self.agent(f"Proporciona clima para {city}")

        return A2AResponse(
            id=request.id,
            action=request.action,
            status="success",
            output={
                "city": city,
                "weather": response
            }
        )


class ActivitiesAgentA2A:
    """Agente de actividades que implementa protocolo A2A"""

    def __init__(self):
        self.agent = Agent(
            system_prompt="""Eres un experto en turismo. Recomiendas actividades
            y lugares interesantes basado en el destino y condiciones."""
        )
        self.agent_id = "activities-agent"

    @property
    def agent_card(self) -> Dict:
        return {
            "name": "Activities Agent",
            "description": "Recomienda actividades y lugares turísticos",
            "agent_id": self.agent_id,
            "version": "1.0.0",
            "actions": [
                {
                    "id": "get_activities",
                    "name": "Get Activities",
                    "description": "Obtiene actividades recomendadas",
                    "parameters": [
                        {
                            "name": "destination",
                            "type": "string",
                            "required": True
                        },
                        {
                            "name": "weather",
                            "type": "string",
                            "required": False
                        }
                    ]
                }
            ]
        }

    def handle_action(self, request: A2ARequest) -> A2AResponse:
        """Procesa una acción A2A"""
        if request.action != "get_activities":
            return A2AResponse(
                id=request.id,
                action=request.action,
                status="error",
                error="Acción no soportada"
            )

        destination = request.input.get("destination")
        weather = request.input.get("weather", "cualquier clima")

        if not destination:
            return A2AResponse(
                id=request.id,
                action=request.action,
                status="error",
                error="Parámetro 'destination' requerido"
            )

        # Usar agente Strands
        response = self.agent(
            f"Recomienda 3 actividades para {destination} con clima {weather}"
        )

        return A2AResponse(
            id=request.id,
            action=request.action,
            status="success",
            output={
                "destination": destination,
                "weather_condition": weather,
                "activities": response
            }
        )


# ============================================================================
# PARTE 4: ORQUESTRADOR DE VIAJES (A2A CLIENT)
# ============================================================================

class TravelPlannerA2A:
    """Orquestrador que coordina múltiples agentes A2A"""

    def __init__(self):
        self.weather_agent = WeatherAgentA2A()
        self.activities_agent = ActivitiesAgentA2A()
        self.authenticator = A2AAuthenticator()
        self.request_history: List[Dict] = []

        self.coordinator = Agent(
            system_prompt="""Eres un planificador de viajes experto.
            Coordinas información de múltiples agentes para crear planes completos."""
        )

    def _call_agent(self, agent, request: A2ARequest) -> A2AResponse:
        """Llama un agente y registra la solicitud"""
        response = agent.handle_action(request)
        self.request_history.append({
            "request": request.to_dict(),
            "response": response.to_dict(),
            "timestamp": datetime.now().isoformat()
        })
        return response

    def plan_trip(self, destination: str):
        """Orquesta un plan de viaje completo"""

        print(f"\n{'='*70}")
        print(f"✈️  PLANIFICADOR DE VIAJES A2A")
        print(f"{'='*70}\n")

        print(f"Destino: {destination}\n")

        # Paso 1: Obtener clima
        print("📡 Paso 1: Consultando clima...")
        weather_request = A2ARequest(
            id=str(uuid.uuid4()),
            action="get_weather",
            input={"city": destination},
            authorization=self.authenticator.create_token("trip-planner", ["weather.read"])
        )

        weather_response = self._call_agent(self.weather_agent, weather_request)

        if weather_response.status == "success":
            print(f"✓ Clima obtenido")
            weather_info = weather_response.output.get("weather", "")
            print(f"  {weather_info}\n")
        else:
            print(f"✗ Error: {weather_response.error}\n")
            weather_info = "desconocido"

        # Paso 2: Obtener actividades
        print("📡 Paso 2: Consultando actividades...")
        activities_request = A2ARequest(
            id=str(uuid.uuid4()),
            action="get_activities",
            input={
                "destination": destination,
                "weather": weather_info
            },
            authorization=self.authenticator.create_token("trip-planner", ["activities.read"])
        )

        activities_response = self._call_agent(self.activities_agent, activities_request)

        if activities_response.status == "success":
            print(f"✓ Actividades obtenidas")
            activities = activities_response.output.get("activities", "")
            print(f"  {activities}\n")
        else:
            print(f"✗ Error: {activities_response.error}\n")

        # Paso 3: Coordinación final
        print("📋 Paso 3: Generando plan de viaje...")
        coordination_summary = self.coordinator(
            f"Resume un plan de viaje a {destination} considerando: clima={weather_info}"
        )
        print(f"✓ Plan generado:\n{coordination_summary}\n")

    def print_request_history(self):
        """Muestra historial de solicitudes A2A"""
        if not self.request_history:
            return

        print(f"\n{'='*70}")
        print("HISTORIAL DE SOLICITUDES A2A")
        print(f"{'='*70}\n")

        for i, entry in enumerate(self.request_history, 1):
            req = entry["request"]
            resp = entry["response"]
            print(f"{i}. {req['action']} → {resp['status']}")
            print(f"   ID: {req['id']}")
            print(f"   Entrada: {req['input']}")
            print()


def main():
    """Ejecuta demostración completa del protocolo A2A"""

    planner = TravelPlannerA2A()

    # Mostrar AgentCards
    print("\n" + "="*70)
    print("AGENTES A2A DISPONIBLES")
    print("="*70 + "\n")

    print("📋 Weather Agent:")
    print(json.dumps(planner.weather_agent.agent_card, indent=2))

    print("\n📋 Activities Agent:")
    print(json.dumps(planner.activities_agent.agent_card, indent=2))

    # Planificar un viaje
    planner.plan_trip("París")

    # Mostrar historial
    planner.print_request_history()

    # Información final
    print("\n" + "="*70)
    print("INFORMACIÓN SOBRE EL PROTOCOLO A2A")
    print("="*70)
    print("""
Este ejemplo demuestra el protocolo A2A de Google:

✓ AgentCards: Descripción de capacidades (/.well-known/agent.json)
✓ Solicitudes A2A: Formato estándar JSON-RPC
✓ Respuestas A2A: Formato estructurado
✓ Autenticación: Tokens JWT
✓ Orquestación: Coordinación entre múltiples agentes

El protocolo A2A permite:
- Descubrimiento automático de agentes
- Comunicación estandarizada
- Seguridad mediante autenticación
- Interoperabilidad entre sistemas
    """)


if __name__ == "__main__":
    main()

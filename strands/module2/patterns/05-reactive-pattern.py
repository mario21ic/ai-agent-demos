"""
Reactive Agent Pattern
======================
Los agentes reaccionan a eventos específicos disparados por el sistema.
Útil para monitoreo, alertas, sistemas en tiempo real, etc.

Use case: Monitoreo de sistemas, alertas, respuesta a incidentes, etc.
"""

from strands import Agent
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Callable


class EventType(Enum):
    """Tipos de eventos que pueden ocurrir"""
    HIGH_LOAD = "high_load"
    LOW_PERFORMANCE = "low_performance"
    SECURITY_ALERT = "security_alert"
    DATA_ANOMALY = "data_anomaly"
    USER_COMPLAINT = "user_complaint"


@dataclass
class Event:
    """Evento que dispara reacciones en agentes"""
    event_type: EventType
    severity: str  # critical, high, medium, low
    description: str
    timestamp: datetime
    data: dict

    def __str__(self):
        return f"[{self.severity.upper()}] {self.event_type.value}: {self.description}"


class ReactiveAgent:
    """Agente que reacciona a eventos específicos"""

    def __init__(self, name: str, system_prompt: str, handles_events: List[EventType]):
        self.name = name
        self.agent = Agent(system_prompt=system_prompt)
        self.handles_events = handles_events
        self.responses: List[str] = []
        self.is_active = True

    def can_handle(self, event: Event) -> bool:
        """Verifica si este agente puede manejar el evento"""
        return event.event_type in self.handles_events and self.is_active

    def react(self, event: Event) -> str:
        """Reacciona a un evento"""

        prompt = f"""
        Evento: {event}
        Severidad: {event.severity}
        Descripción: {event.description}

        Detalles técnicos:
        {event.data}

        Proporciona una respuesta concisa y actionable:
        1. Análisis del problema
        2. Acciones inmediatas
        3. Seguimiento
        """

        response = self.agent(prompt)
        self.responses.append(response)
        return response


class ReactiveSystem:
    """Sistema que monitorea eventos y coordina reacciones"""

    def __init__(self):
        # Agentes especializados que reaccionan a eventos
        self.load_monitor = ReactiveAgent(
            name="Load Monitor",
            system_prompt="Eres un especialista en performance. Respondes a eventos de carga.",
            handles_events=[EventType.HIGH_LOAD, EventType.LOW_PERFORMANCE]
        )

        self.security_monitor = ReactiveAgent(
            name="Security Monitor",
            system_prompt="Eres un especialista en seguridad. Respondes a alertas de seguridad.",
            handles_events=[EventType.SECURITY_ALERT]
        )

        self.analytics_monitor = ReactiveAgent(
            name="Analytics Monitor",
            system_prompt="Eres un especialista en datos. Respondes a anomalías de datos.",
            handles_events=[EventType.DATA_ANOMALY]
        )

        self.customer_support = ReactiveAgent(
            name="Customer Support",
            system_prompt="Eres un especialista en experiencia del cliente. Respondes a quejas.",
            handles_events=[EventType.USER_COMPLAINT]
        )

        self.agents = [
            self.load_monitor,
            self.security_monitor,
            self.analytics_monitor,
            self.customer_support
        ]

        self.event_queue: List[Event] = []
        self.event_log: List[tuple] = []  # (event, responses)

    def enqueue_event(self, event: Event):
        """Añade un evento a la cola"""
        self.event_queue.append(event)

    def process_event(self, event: Event):
        """Procesa un evento y coordina reacciones"""

        print(f"\n📢 {event}")
        print("-" * 70)

        responses = []

        # Todos los agentes que pueden manejar este evento reaccionan
        for agent in self.agents:
            if agent.can_handle(event):
                print(f"  {agent.name}:")
                response = agent.react(event)
                print(f"    {response[:100]}...")
                responses.append({
                    "agent": agent.name,
                    "response": response
                })

        self.event_log.append((event, responses))

        if not responses:
            print("  ⚠️ No hay agentes disponibles para este evento")

    def process_all_events(self):
        """Procesa todos los eventos en la cola"""

        print(f"\n{'='*70}")
        print(f"REACTIVE SYSTEM - Processing {len(self.event_queue)} events")
        print(f"{'='*70}\n")

        while self.event_queue:
            event = self.event_queue.pop(0)
            self.process_event(event)

    def simulate_incidents(self):
        """Simula un conjunto de incidentes"""

        print(f"\n{'='*70}")
        print("SIMULATING INCIDENTS")
        print(f"{'='*70}\n")

        # Simular eventos
        events = [
            Event(
                event_type=EventType.HIGH_LOAD,
                severity="critical",
                description="CPU usage at 95%",
                timestamp=datetime.now(),
                data={"cpu": 95, "memory": 78, "requests": 5000}
            ),
            Event(
                event_type=EventType.SECURITY_ALERT,
                severity="high",
                description="Suspicious login attempts detected",
                timestamp=datetime.now(),
                data={"failed_attempts": 50, "unique_ips": 10, "location": "unusual"}
            ),
            Event(
                event_type=EventType.DATA_ANOMALY,
                severity="medium",
                description="Unusual pattern in transaction data",
                timestamp=datetime.now(),
                data={"avg_transaction": 150, "spike": 5000, "count": 1}
            ),
            Event(
                event_type=EventType.USER_COMPLAINT,
                severity="high",
                description="Multiple users reporting slow response times",
                timestamp=datetime.now(),
                data={"complaints": 15, "avg_response_time": 5.2, "expected": 0.5}
            ),
            Event(
                event_type=EventType.LOW_PERFORMANCE,
                severity="medium",
                description="Database query performance degradation",
                timestamp=datetime.now(),
                data={"query_time": 3.5, "normal": 0.2, "affected_tables": ["users", "orders"]}
            ),
        ]

        # Encolar eventos
        for event in events:
            self.enqueue_event(event)

        # Procesar
        self.process_all_events()

    def print_system_status(self):
        """Imprime estado del sistema"""

        print(f"\n{'='*70}")
        print("REACTIVE SYSTEM STATUS")
        print(f"{'='*70}\n")

        print("Agentes monitoreando:")
        for agent in self.agents:
            status = "✓ ACTIVE" if agent.is_active else "✗ INACTIVE"
            handles = ", ".join([e.value for e in agent.handles_events])
            print(f"  {status} {agent.name}")
            print(f"    Eventos: {handles}")
            print(f"    Respuestas: {len(agent.responses)}")
            print()

        print(f"Total de eventos procesados: {len(self.event_log)}")

        print("\n" + "="*70)
        print("REACTIVE PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Respuesta rápida a eventos
  ✓ Escalable (nuevos agentes = nuevos tipos de eventos)
  ✓ Desacoplamiento entre componentes
  ✓ Ideal para sistemas en tiempo real
  ✓ Cada agente solo hace su especialidad

Desventajas:
  ✗ Complejo de debuggear
  ✗ Orden de procesamiento puede importar
  ✗ Requiere buena orquestación de eventos
        """)


def main():
    """Ejecuta ejemplo del patrón reactivo"""

    system = ReactiveSystem()

    # Simular incidentes
    system.simulate_incidents()

    # Mostrar estado
    system.print_system_status()


if __name__ == "__main__":
    main()

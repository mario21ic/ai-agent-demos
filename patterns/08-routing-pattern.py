"""
Routing/Router Agent Pattern
=============================
Un agente "router" dirige solicitudes al agente especializado correcto.
Optimiza eficiencia enviando cada tarea al experto adecuado.

Use case: Sistemas de soporte, delegación inteligente, etc.
"""

from strands import Agent
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class TaskCategory(Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    LEGAL = "legal"
    FINANCIAL = "financial"
    CREATIVE = "creative"
    UNKNOWN = "unknown"


@dataclass
class Request:
    """Una solicitud a ser ruteada"""
    id: str
    content: str
    category: TaskCategory = None


@dataclass
class RoutingDecision:
    """Decisión de enrutamiento"""
    request_id: str
    assigned_agent: str
    reasoning: str
    confidence: float


class RouterAgent:
    """Agente que rutea solicitudes a especialistas"""

    def __init__(self):
        # Router central
        self.router = Agent(
            system_prompt="""Eres un router inteligente.
            Tu trabajo es:
            1. Analizar solicitudes
            2. Determinar la categoría/tipo
            3. Identificar al especialista correcto
            4. Justificar tu decisión

            Sé preciso en la clasificación."""
        )

        # Especialistas
        self.technical_agent = Agent(
            system_prompt="Eres un especialista técnico. Resuelves problemas técnicos."
        )

        self.business_agent = Agent(
            system_prompt="Eres un especialista en negocios. Ayudas con estrategia y operaciones."
        )

        self.legal_agent = Agent(
            system_prompt="Eres un especialista legal. Manejas asuntos legales."
        )

        self.financial_agent = Agent(
            system_prompt="Eres un especialista financiero. Asesoras sobre finanzas."
        )

        self.creative_agent = Agent(
            system_prompt="Eres un especialista creativo. Generas contenido creativo."
        )

        self.specialists = {
            TaskCategory.TECHNICAL: ("Technical Specialist", self.technical_agent),
            TaskCategory.BUSINESS: ("Business Specialist", self.business_agent),
            TaskCategory.LEGAL: ("Legal Specialist", self.legal_agent),
            TaskCategory.FINANCIAL: ("Financial Specialist", self.financial_agent),
            TaskCategory.CREATIVE: ("Creative Specialist", self.creative_agent),
        }

        self.routing_log: List[RoutingDecision] = []
        self.request_log: List[Dict] = []

    def classify_request(self, request: Request) -> TaskCategory:
        """Clasifica una solicitud en categoría"""

        classification_prompt = f"""
        Solicitud: {request.content}

        Clasifica esta solicitud en UNA de estas categorías:
        - TECHNICAL: Problemas técnicos, programming, infraestructura
        - BUSINESS: Estrategia, operaciones, management
        - LEGAL: Asuntos legales, contratos, compliance
        - FINANCIAL: Finanzas, inversión, presupuesto
        - CREATIVE: Contenido creativo, diseño, marketing

        Proporciona:
        1. Categoría
        2. Confianza (1-100%)
        3. Razón breve

        Formato:
        CATEGORIA: ...
        CONFIANZA: ...%
        RAZON: ...
        """

        classification = self.router(classification_prompt)

        # Parsear respuesta
        lines = classification.split('\n')
        category_str = "UNKNOWN"
        confidence_str = "50"

        for line in lines:
            if "CATEGORIA:" in line:
                category_str = line.split(":")[-1].strip().upper()
            elif "CONFIANZA:" in line:
                confidence_str = line.split(":")[-1].replace("%", "").strip()

        # Mapear a enum
        try:
            category = TaskCategory[category_str]
        except:
            category = TaskCategory.UNKNOWN

        try:
            confidence = int(confidence_str) / 100
        except:
            confidence = 0.5

        return category

    def route_request(self, request: Request) -> RoutingDecision:
        """Rutea una solicitud al especialista correcto"""

        print(f"\n{'='*70}")
        print(f"ROUTING REQUEST: {request.id}")
        print(f"{'='*70}\n")

        print(f"Request: {request.content}\n")

        # Fase 1: Clasificación
        print("📊 PHASE 1: Classification")
        print("-" * 70)

        category = self.classify_request(request)
        print(f"Category: {category.value}")

        # Fase 2: Selección de especialista
        print("\n🎯 PHASE 2: Specialist Selection")
        print("-" * 70)

        if category in self.specialists:
            specialist_name, specialist_agent = self.specialists[category]
            confidence = 0.9
        else:
            # Si categoría desconocida, usar router como fallback
            specialist_name = "General Router"
            specialist_agent = self.router
            confidence = 0.5

        print(f"Assigned To: {specialist_name}")
        print(f"Confidence: {confidence*100:.0f}%\n")

        # Fase 3: Ejecución en especialista
        print("✅ PHASE 3: Specialist Execution")
        print("-" * 70)

        execution_prompt = f"Solicitud: {request.content}\n\nResuelve esto según tu especialidad."
        response = specialist_agent(execution_prompt)
        print(f"Response: {response[:150]}...\n")

        # Crear decisión de enrutamiento
        decision = RoutingDecision(
            request_id=request.id,
            assigned_agent=specialist_name,
            reasoning=f"Clasificado como {category.value}",
            confidence=confidence
        )

        self.routing_log.append(decision)

        # Registrar
        self.request_log.append({
            "request": request,
            "category": category,
            "specialist": specialist_name,
            "response": response
        })

        return decision

    def route_batch(self, requests: List[Request]):
        """Rutea múltiples solicitudes"""

        print(f"\n{'='*70}")
        print(f"BATCH ROUTING - {len(requests)} requests")
        print(f"{'='*70}\n")

        decisions = []
        for request in requests:
            decision = self.route_request(request)
            decisions.append(decision)

        return decisions

    def print_routing_summary(self):
        """Imprime resumen de enrutamiento"""

        print(f"\n{'='*70}")
        print("ROUTING SUMMARY")
        print(f"{'='*70}\n")

        if not self.routing_log:
            print("No routing decisions yet\n")
            return

        print(f"Total Requests Routed: {len(self.routing_log)}")

        # Por especialista
        specialists_count = {}
        for decision in self.routing_log:
            specialist = decision.assigned_agent
            specialists_count[specialist] = specialists_count.get(specialist, 0) + 1

        print("\nRequests by Specialist:")
        for specialist, count in specialists_count.items():
            percentage = (count / len(self.routing_log)) * 100
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            print(f"  {specialist:25} [{bar}] {count} ({percentage:.0f}%)")

        # Confianza promedio
        avg_confidence = sum([d.confidence for d in self.routing_log]) / len(self.routing_log)
        print(f"\nAverage Routing Confidence: {avg_confidence*100:.1f}%")

        # Categorías
        print("\nRouting Decisions:")
        for i, decision in enumerate(self.routing_log, 1):
            confidence_indicator = "✓" if decision.confidence > 0.8 else "~"
            print(f"{i}. {confidence_indicator} {decision.assigned_agent} (confidence: {decision.confidence*100:.0f}%)")

        print("\n" + "="*70)
        print("ROUTING PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Optimiza eficiencia
  ✓ Dirige al especialista correcto
  ✓ Escalable
  ✓ Mejora con feedback
  ✓ Reduce latencia

Desventajas:
  ✗ Clasificación imperfecta
  ✗ Overhead de clasificación
  ✗ Posibles falsos encaminamientos
  ✗ Requiere especialistas bien definidos

Casos de Uso:
  • Customer support routing
  • Task delegation
  • Load balancing
  • Service distribution
  • Intelligent queuing
        """)


def main():
    """Ejecuta ejemplo del Routing Pattern"""

    router = RouterAgent()

    # Crear solicitudes de prueba
    requests = [
        Request(
            id="r1",
            content="¿Cómo configuro un servidor Kubernetes en producción?"
        ),
        Request(
            id="r2",
            content="¿Cuál debería ser nuestra estrategia de precios para Q4?"
        ),
        Request(
            id="r3",
            content="Necesito ayuda con un contrato de licencia de software"
        ),
        Request(
            id="r4",
            content="¿Qué presupuesto deberíamos asignar para marketing?"
        ),
        Request(
            id="r5",
            content="Ayúdame a escribir un poema sobre la primavera"
        ),
    ]

    # Rutear todos
    router.route_batch(requests)

    # Resumen
    router.print_routing_summary()


if __name__ == "__main__":
    main()

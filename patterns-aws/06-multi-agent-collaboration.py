"""
AWS Pattern: Multi-agent Collaboration
=======================================
Múltiples agentes colaboran, negocian y alcanzan consenso
para resolver problemas complejos.

Principios AWS:
- Asincrónico: Agentes trabajan en paralelo
- Autonomía: Cada agente actúa independientemente
- Agencia: Colaboración para objetivo común
"""

from strands import Agent
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    PROPOSAL = "proposal"
    EVALUATION = "evaluation"
    OBJECTION = "objection"
    CONSENSUS = "consensus"
    DECISION = "decision"


@dataclass
class Message:
    """Mensaje entre agentes"""
    sender: str
    recipient: str
    message_type: MessageType
    content: str
    timestamp: str = None


class CollaborativeAgent:
    """Agente que colabora con otros"""

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.agent = Agent(
            system_prompt=f"""Eres {name}, especialista en {specialty}.
            Tu rol es colaborar con otros agentes para resolver problemas.
            Sé específico, conciso y constructivo."""
        )
        self.messages_sent: List[Message] = []
        self.messages_received: List[Message] = []

    def propose_solution(self, problem: str) -> str:
        """Propone una solución"""
        prompt = f"""
        Problema: {problem}

        Como especialista en {self.specialty}, propón:
        1. Tu solución recomendada
        2. Ventajas de tu enfoque
        3. Posibles limitaciones
        4. Recursos requeridos
        """
        return self.agent(prompt)

    def evaluate_proposal(self, proposal: str, problem: str) -> str:
        """Evalúa una propuesta de otro agente"""
        prompt = f"""
        Propuesta de otro especialista:
        {proposal}

        Problema original: {problem}

        Evalúa esta propuesta desde la perspectiva de {self.specialty}:
        1. Fortalezas
        2. Debilidades
        3. Cómo mejorarla
        4. Impacto en mi dominio
        """
        return self.agent(prompt)

    def send_message(self, recipient: str, message_type: MessageType, content: str) -> Message:
        """Envía un mensaje a otro agente"""
        msg = Message(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content
        )
        self.messages_sent.append(msg)
        return msg

    def receive_message(self, msg: Message):
        """Recibe un mensaje de otro agente"""
        self.messages_received.append(msg)


class MultiAgentCollaborationSystem:
    """Sistema de colaboración multi-agente"""

    def __init__(self):
        # Crear agentes especializados
        self.backend_engineer = CollaborativeAgent(
            "Backend Engineer",
            "backend architecture and scalability"
        )

        self.frontend_engineer = CollaborativeAgent(
            "Frontend Engineer",
            "user experience and interface design"
        )

        self.devops_engineer = CollaborativeAgent(
            "DevOps Engineer",
            "infrastructure and deployment"
        )

        self.security_specialist = CollaborativeAgent(
            "Security Specialist",
            "security and compliance"
        )

        self.agents = [
            self.backend_engineer,
            self.frontend_engineer,
            self.devops_engineer,
            self.security_specialist
        ]

        self.facilitator = Agent(
            system_prompt="""Eres facilitador de colaboración.
            Tu rol es:
            1. Sintetizar propuestas
            2. Identificar puntos de acuerdo
            3. Resolver conflictos
            4. Llegar a consenso

            Sé imparcial y constructivo."""
        )

        self.collaboration_log: List[Dict] = []

    def collaboration_round(self, problem: str, round_num: int):
        """Una ronda de colaboración"""

        print(f"\n🔄 COLLABORATION ROUND {round_num}")
        print("-" * 70)

        # Fase 1: Propuestas
        print("\n1️⃣ PROPOSALS")
        proposals = {}

        for agent in self.agents:
            print(f"\n  {agent.name}:")
            proposal = agent.propose_solution(problem)
            proposals[agent.name] = proposal
            print(f"    {proposal[:100]}...")

        # Fase 2: Evaluaciones cruzadas
        print(f"\n2️⃣ EVALUATIONS")

        evaluations = {}
        for proposer_name, proposal in proposals.items():
            print(f"\n  Evaluating {proposer_name}'s proposal:")

            evaluations[proposer_name] = []

            for evaluator in self.agents:
                if evaluator.name != proposer_name:
                    eval_result = evaluator.evaluate_proposal(proposal, problem)
                    evaluations[proposer_name].append({
                        "evaluator": evaluator.name,
                        "evaluation": eval_result
                    })
                    print(f"    {evaluator.name}: {eval_result[:80]}...")

        # Fase 3: Consenso
        print(f"\n3️⃣ CONSENSUS BUILDING")

        synthesis_prompt = f"""
        Múltiples propuestas fueron evaluadas:

        {chr(10).join([f"- {name}: {prop[:100]}..." for name, prop in proposals.items()])}

        Objetivo: Sintetizar estas propuestas en una solución consensuada.

        Proporciona:
        1. Puntos de acuerdo entre todas las propuestas
        2. Puntos de desacuerdo críticos
        3. Solución integrada que incorpore lo mejor de cada enfoque
        4. Recomendación final
        """

        consensus = self.facilitator(synthesis_prompt)
        print(f"\nConsensus:\n{consensus}\n")

        return {
            "round": round_num,
            "proposals": proposals,
            "evaluations": evaluations,
            "consensus": consensus
        }

    def resolve_conflict(self, conflict_description: str):
        """Resuelve un conflicto entre agentes"""

        print(f"\n⚖️ CONFLICT RESOLUTION")
        print("-" * 70)
        print(f"Conflict: {conflict_description}\n")

        # Obtener perspectivas
        perspectives = {}
        for agent in self.agents:
            perspective_prompt = f"""
            Conflicto: {conflict_description}

            ¿Cuál es tu perspectiva como {agent.specialty}?
            Sé honesto sobre:
            1. Tus preocupaciones
            2. Qué es no-negociable para ti
            3. Dónde podrías ser flexible
            """
            perspectives[agent.name] = agent.agent(perspective_prompt)

        print("Perspectives:")
        for agent_name, perspective in perspectives.items():
            print(f"\n  {agent_name}:")
            print(f"  {perspective[:100]}...\n")

        # Resolver
        resolution_prompt = f"""
        Conflicto: {conflict_description}

        Perspectivas de cada especialista:
        {chr(10).join([f"- {name}: {per[:80]}..." for name, per in perspectives.items()])}

        Proporciona:
        1. Raíz del conflicto
        2. Intereses comunes
        3. Solución de compromiso
        4. Plan de implementación
        """

        resolution = self.facilitator(resolution_prompt)
        print(f"Resolution:\n{resolution}\n")

    def full_collaboration_scenario(self):
        """Ejecuta un escenario de colaboración completo"""

        print(f"\n{'='*70}")
        print("MULTI-AGENT COLLABORATION SYSTEM")
        print(f"{'='*70}\n")

        problem = """
        Diseñar un nuevo sistema de microservicios para una plataforma de e-commerce
        que sea:
        - Altamente escalable (millones de usuarios)
        - Seguro (PCI-DSS, GDPR)
        - Rápido (latencia < 100ms)
        - Económico (minimizar costos de infraestructura)
        """

        print(f"Problem to Solve:\n{problem}\n")

        # Ronda 1
        log1 = self.collaboration_round(problem, 1)

        # Ronda 2: Refinamiento
        refined_problem = f"""
        {problem}

        Feedback de la ronda anterior:
        {log1['consensus'][:200]}...

        Cómo refinarías tu propuesta considerando este feedback?
        """

        log2 = self.collaboration_round(refined_problem, 2)

        # Guardar registro
        self.collaboration_log.append(log1)
        self.collaboration_log.append(log2)

        # Manejo de conflicto
        self.resolve_conflict(
            "Backend Engineer quiere usar serverless pero DevOps prefiere Kubernetes"
        )

    def print_collaboration_summary(self):
        """Imprime resumen de la colaboración"""

        print(f"\n{'='*70}")
        print("COLLABORATION SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total Collaboration Rounds: {len(self.collaboration_log)}")

        print("\nAgents Involved:")
        for agent in self.agents:
            print(f"  • {agent.name}")
            print(f"    Specialty: {agent.specialty}")
            print(f"    Messages Sent: {len(agent.messages_sent)}")
            print(f"    Messages Received: {len(agent.messages_received)}")

        print("\n" + "="*70)
        print("MULTI-AGENT COLLABORATION CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Perspectivas diversas
  ✓ Soluciones más completas
  ✓ Detección de conflictos temprana
  ✓ Mayor aceptación de decisiones
  ✓ Conocimiento colectivo

Desventajas:
  ✗ Lento (múltiples rondas)
  ✗ Complejo de coordinar
  ✗ Puede llevar a conformismo
  ✗ Comunicación crítica

AWS Pattern: MULTI-AGENT COLLABORATION
  → Amazon Bedrock para coordinación
  → EventBridge para comunicación
  → DynamoDB para estado compartido
  → SQS para colas de mensajes

Casos de Uso:
  • Toma de decisiones organizacional
  • Diseño de arquitectura
  • Revisión de seguridad
  • Análisis de impacto
  • Resolución de conflictos
        """)


def main():
    """Ejecuta ejemplo de Multi-agent Collaboration"""

    system = MultiAgentCollaborationSystem()

    # Escenario de colaboración completo
    system.full_collaboration_scenario()

    # Resumen
    system.print_collaboration_summary()


if __name__ == "__main__":
    main()

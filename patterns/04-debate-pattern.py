"""
Debate/Consensus Agent Pattern
================================
Múltiples agentes con diferentes perspectivas debaten para llegar a un consenso.
Útil para toma de decisiones, brainstorming, resolución de conflictos, etc.

Use case: Decisiones importantes, análisis de riesgos, validación de ideas, etc.
"""

from strands import Agent
from typing import List, Dict


class DebateParticipant:
    """Participante en un debate"""

    def __init__(self, name: str, perspective: str, agent: Agent):
        self.name = name
        self.perspective = perspective
        self.agent = agent
        self.arguments: List[str] = []
        self.vote = None

    def present_argument(self, topic: str, previous_arguments: str = "") -> str:
        """Presenta un argumento"""

        prompt = f"""
        Eres {self.name}. Tu perspectiva: {self.perspective}

        Tema a debatir: {topic}

        {f"Argumentos previos: {previous_arguments}" if previous_arguments else ""}

        Proporciona un argumento claro y conciso a favor de tu perspectiva.
        Sé breve (2-3 puntos clave). Contesta solo el argumento sin más texto.
        """

        argument = self.agent(prompt)
        self.arguments.append(argument)
        return argument

    def cast_vote(self, topic: str, all_arguments: str) -> str:
        """Vota basado en todos los argumentos"""

        prompt = f"""
        Eres {self.name}. Tu perspectiva inicial: {self.perspective}

        Después de escuchar todos estos argumentos:
        {all_arguments}

        ¿Cuál es tu voto final? ¿A favor o en contra?
        Justifica tu voto en una sola frase.
        """

        vote = self.agent(prompt)
        self.vote = vote
        return vote


class DebateSession:
    """Sesión de debate entre múltiples agentes"""

    def __init__(self):
        # Debatientes con diferentes perspectivas
        self.proponent = DebateParticipant(
            name="Alex (Proponente)",
            perspective="Entusiasta de la innovación, cree en el cambio",
            agent=Agent(system_prompt="Eres optimista y ves oportunidades")
        )

        self.skeptic = DebateParticipant(
            name="Jordan (Escéptico)",
            perspective="Analítico y cauteloso, enfocado en riesgos",
            agent=Agent(system_prompt="Eres cauteloso y cuestiona todo")
        )

        self.pragmatist = DebateParticipant(
            name="Casey (Pragmático)",
            perspective="Práctico, enfocado en resultados y viabilidad",
            agent=Agent(system_prompt="Eres pragmático y enfocado en resultados")
        )

        self.participants = [self.proponent, self.skeptic, self.pragmatist]
        self.moderator = Agent(
            system_prompt="""Eres un moderador neutral e imparcial.
            Tu trabajo es resumir puntos de vista, identificar consensos
            y hacer preguntas clarificadoras."""
        )

        self.debate_log: List[Dict] = []

    def run_debate(self, topic: str, rounds: int = 3) -> Dict:
        """Ejecuta un debate de múltiples rondas"""

        print(f"\n{'='*70}")
        print(f"DEBATE SESSION: {topic}")
        print(f"{'='*70}\n")

        # Ronda de apertura
        print("📢 RONDA DE APERTURA")
        print("-" * 70)

        opening_arguments = []

        for participant in self.participants:
            print(f"\n{participant.name}:")
            argument = participant.present_argument(topic)
            print(f"  {argument}")
            opening_arguments.append(f"{participant.name}: {argument}")

        # Rondas de debate
        for round_num in range(1, rounds + 1):
            print(f"\n\n💬 RONDA {round_num}")
            print("-" * 70)

            previous_args = "\n".join(opening_arguments)

            for participant in self.participants:
                print(f"\n{participant.name}:")
                argument = participant.present_argument(
                    topic,
                    previous_args
                )
                print(f"  {argument}")

        # Ronda de votación
        print(f"\n\n🗳️  RONDA DE VOTACIÓN")
        print("-" * 70)

        all_arguments = "\n".join(
            [f"{p.name}: {arg}" for p in self.participants for arg in p.arguments]
        )

        votes = []
        for participant in self.participants:
            print(f"\n{participant.name}:")
            vote = participant.cast_vote(topic, all_arguments)
            print(f"  {vote}")
            votes.append(vote)

        # Conclusiones del moderador
        print(f"\n\n📋 CONCLUSIONES DEL MODERADOR")
        print("-" * 70)

        summary_prompt = f"""
        Resume este debate sobre: {topic}

        Perspectivas:
        {all_arguments}

        Votos finales:
        {chr(10).join(votes)}

        Proporciona:
        1. Puntos de acuerdo
        2. Puntos de desacuerdo
        3. Consenso alcanzado (si existe)
        4. Recomendación final
        """

        conclusion = self.moderator(summary_prompt)

        print(f"Resumen:\n{conclusion}")

        return {
            "topic": topic,
            "participants": len(self.participants),
            "rounds": rounds,
            "votes": votes,
            "conclusion": conclusion
        }

    def print_debate_statistics(self):
        """Imprime estadísticas del debate"""

        print(f"\n{'='*70}")
        print("DEBATE STATISTICS")
        print(f"{'='*70}\n")

        print("Participantes:")
        for i, participant in enumerate(self.participants, 1):
            print(f"{i}. {participant.name}")
            print(f"   Perspectiva: {participant.perspective}")
            print(f"   Argumentos presentados: {len(participant.arguments)}")
            print(f"   Voto: {participant.vote}")
            print()

        print("\n" + "="*70)
        print("DEBATE PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Múltiples perspectivas consideradas
  ✓ Decisiones bien fundamentadas
  ✓ Identifica riesgos y oportunidades
  ✓ Genera consenso o clarifica desacuerdos
  ✓ Ideal para decisiones complejas

Desventajas:
  ✗ Consume tiempo
  ✗ Puede llevar a parálisis por análisis
  ✗ Requiere moderador imparcial
        """)


def main():
    """Ejecuta ejemplo del patrón de debate"""

    debate = DebateSession()

    topic = "¿Debería una empresa adoptar completamente trabajo remoto?"

    result = debate.run_debate(topic, rounds=2)

    debate.print_debate_statistics()


if __name__ == "__main__":
    main()

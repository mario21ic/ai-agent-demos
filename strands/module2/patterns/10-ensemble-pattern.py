"""
Ensemble Agent Pattern
======================
Múltiples agentes independientes responden la misma pregunta,
luego se combinan/votan para obtener una respuesta robusta.

Use case: Decisiones críticas, predicciones, etc.
"""

from strands import Agent
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class VotingMethod(Enum):
    MAJORITY = "majority"  # Mayoría simple
    WEIGHTED = "weighted"  # Ponderado por confianza
    UNANIMOUS = "unanimous"  # Requiere consenso
    AVERAGED = "averaged"  # Promedio de respuestas


@dataclass
class AgentOpinion:
    """Opinión de un agente"""
    agent_name: str
    response: str
    confidence: float  # 0-1
    reasoning: str


class EnsembleAgent:
    """Sistema de ensemble de múltiples agentes"""

    def __init__(self, voting_method: VotingMethod = VotingMethod.MAJORITY):
        # Crear ensemble de agentes independientes
        self.conservative = Agent(
            system_prompt="""Eres un pensador conservador.
            Prefieres soluciones seguras, comprobadas.
            Eres escéptico de lo nuevo.
            Proporciona respuestas con advertencias de riesgo."""
        )

        self.optimistic = Agent(
            system_prompt="""Eres un pensador optimista.
            Ves oportunidades donde otros ven riesgos.
            Eres entusiasta de nuevas ideas.
            Proporciona respuestas con énfasis en beneficios."""
        )

        self.analytical = Agent(
            system_prompt="""Eres un analista riguroso.
            Basas tus respuestas en datos y lógica.
            Eres objetivo e imparcial.
            Proporciona respuestas con análisis detallado."""
        )

        self.pragmatic = Agent(
            system_prompt="""Eres un pragmático.
            Te enfocas en viabilidad y resultados prácticos.
            Balanceas teoría con realidad.
            Proporciona respuestas orientadas a implementación."""
        )

        self.ensemble_members = [
            ("Conservative", self.conservative),
            ("Optimistic", self.optimistic),
            ("Analytical", self.analytical),
            ("Pragmatic", self.pragmatic),
        ]

        self.voting_method = voting_method
        self.opinions_log: List[Dict] = []

    def get_ensemble_opinions(self, question: str) -> List[AgentOpinion]:
        """Obtiene opiniones de todos los miembros del ensemble"""

        print(f"\n{'='*70}")
        print(f"ENSEMBLE VOTING")
        print(f"{'='*70}\n")

        print(f"Question: {question}\n")
        print("📊 GATHERING OPINIONS")
        print("-" * 70)

        opinions = []

        for agent_name, agent in self.ensemble_members:
            print(f"\n{agent_name} Agent:")

            # Pedir respuesta y confianza
            prompt = f"""
            Pregunta: {question}

            Responde:
            1. Tu respuesta/recomendación
            2. Tu nivel de confianza (0-100%)
            3. Tu razonamiento en una frase

            Formato:
            RESPUESTA: ...
            CONFIANZA: ...%
            RAZONAMIENTO: ...
            """

            response = agent(prompt)

            # Parsear
            lines = response.split('\n')
            answer = ""
            confidence = 50
            reasoning = ""

            for line in lines:
                if "RESPUESTA:" in line:
                    answer = line.split(":")[-1].strip()
                elif "CONFIANZA:" in line:
                    conf_str = line.split(":")[-1].replace("%", "").strip()
                    try:
                        confidence = int(conf_str) / 100
                    except:
                        confidence = 0.5
                elif "RAZONAMIENTO:" in line:
                    reasoning = line.split(":")[-1].strip()

            opinion = AgentOpinion(
                agent_name=agent_name,
                response=answer,
                confidence=confidence,
                reasoning=reasoning
            )
            opinions.append(opinion)

            print(f"  Response: {answer[:60]}...")
            print(f"  Confidence: {confidence*100:.0f}%")
            print(f"  Reasoning: {reasoning[:60]}...")

        return opinions

    def synthesize_opinions(self, opinions: List[AgentOpinion], question: str) -> str:
        """Sintetiza opiniones usando el método de votación"""

        print(f"\n{'='*70}")
        print(f"SYNTHESIZING OPINIONS ({self.voting_method.value})")
        print(f"{'='*70}\n")

        # Crear sumario de opiniones
        opinions_text = "\n".join([
            f"{o.agent_name}: {o.response} (confidence: {o.confidence*100:.0f}%)"
            for o in opinions
        ])

        synthesis_prompt = f"""
        Pregunta: {question}

        Opiniones del ensemble:
        {opinions_text}

        Método de síntesis: {self.voting_method.value}

        Sintetiza estas opiniones en:
        1. Una respuesta final clara
        2. Puntos de acuerdo
        3. Puntos de desacuerdo
        4. Recomendación final

        Considera:
        - La confianza de cada agente
        - Consenso vs divergencia
        - Perspectivas balanceadas
        """

        synthesis = Agent(
            system_prompt="Eres un sintetizador imparcial de opiniones"
        )(synthesis_prompt)

        print(f"Synthesis:\n{synthesis[:300]}...\n")

        return synthesis

    def measure_ensemble_agreement(self, opinions: List[AgentOpinion]) -> Dict:
        """Mide el grado de acuerdo en el ensemble"""

        print(f"\n{'='*70}")
        print("ENSEMBLE AGREEMENT ANALYSIS")
        print(f"{'='*70}\n")

        # Confianza promedio
        avg_confidence = sum([o.confidence for o in opinions]) / len(opinions)

        # Similaridad de respuestas
        responses = [o.response for o in opinions]
        unique_responses = len(set(responses))

        # Puntuación de acuerdo (0-1)
        # Mayor diversidad = menor acuerdo
        agreement = 1 - (unique_responses / len(opinions))

        print(f"Average Confidence: {avg_confidence*100:.1f}%")
        print(f"Unique Responses: {unique_responses}/{len(opinions)}")
        print(f"Agreement Score: {agreement*100:.0f}%")

        if agreement > 0.75:
            agreement_level = "Very High - Consensus"
        elif agreement > 0.5:
            agreement_level = "High - Good alignment"
        elif agreement > 0.25:
            agreement_level = "Moderate - Some divergence"
        else:
            agreement_level = "Low - Significant disagreement"

        print(f"Agreement Level: {agreement_level}\n")

        return {
            "avg_confidence": avg_confidence,
            "unique_responses": unique_responses,
            "agreement_score": agreement,
            "agreement_level": agreement_level
        }

    def full_ensemble_query(self, question: str) -> Dict:
        """Ejecuta una consulta completa del ensemble"""

        # Obtener opiniones
        opinions = self.get_ensemble_opinions(question)

        # Analizar acuerdo
        agreement_analysis = self.measure_ensemble_agreement(opinions)

        # Sintetizar
        synthesis = self.synthesize_opinions(opinions, question)

        # Registrar
        self.opinions_log.append({
            "question": question,
            "opinions": opinions,
            "agreement": agreement_analysis,
            "synthesis": synthesis
        })

        return {
            "opinions": opinions,
            "agreement": agreement_analysis,
            "synthesis": synthesis
        }

    def print_ensemble_summary(self):
        """Imprime resumen del ensemble"""

        print(f"\n{'='*70}")
        print("ENSEMBLE SUMMARY")
        print(f"{'='*70}\n")

        if not self.opinions_log:
            print("No queries logged\n")
            return

        print(f"Total Queries: {len(self.opinions_log)}")
        print(f"Voting Method: {self.voting_method.value}\n")

        # Estadísticas de acuerdo
        all_agreements = [log["agreement"]["agreement_score"] for log in self.opinions_log]
        avg_agreement = sum(all_agreements) / len(all_agreements)

        print(f"Average Agreement Across Queries: {avg_agreement*100:.0f}%")

        # Por query
        print("\nQueries:")
        for i, log in enumerate(self.opinions_log, 1):
            print(f"{i}. {log['question'][:50]}...")
            print(f"   Agreement: {log['agreement']['agreement_level']}")

        print("\n" + "="*70)
        print("ENSEMBLE PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Reduce bias individual
  ✓ Decisiones más robustas
  ✓ Múltiples perspectivas
  ✓ Mejor para problemas complejos
  ✓ Detección de desacuerdos

Desventajas:
  ✗ Costo computacional (múltiples agentes)
  ✗ Lentitud
  ✗ Posible promediación de errores
  ✗ Complejo de implementar

Casos de Uso:
  • Decisiones críticas
  • Predicciones importantes
  • Análisis de riesgos
  • Validación de recomendaciones
  • Sistemas de votación
        """)


def main():
    """Ejecuta ejemplo del Ensemble Pattern"""

    ensemble = EnsembleAgent(voting_method=VotingMethod.WEIGHTED)

    # Preguntas para el ensemble
    questions = [
        "¿Debería una startup invertir en expandir internacionalmente ahora?",
        "¿Es seguro migrar a una arquitectura de microservicios?",
    ]

    for question in questions:
        result = ensemble.full_ensemble_query(question)

    # Resumen
    ensemble.print_ensemble_summary()


if __name__ == "__main__":
    main()

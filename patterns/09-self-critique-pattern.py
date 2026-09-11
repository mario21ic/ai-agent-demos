"""
Self-Critique/Reflection Agent Pattern
=======================================
Un agente genera una respuesta, luego se auto-critica y mejora.
Itera hasta alcanzar calidad aceptable.

Use case: Mejora iterativa de calidad, escritura creativa, etc.
"""

from strands import Agent
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class CritiqueResult:
    """Resultado de una crítica"""
    iteration: int
    content: str
    critique: str
    score: float  # 0-100
    issues_found: List[str]
    improvements_made: List[str]
    ready: bool


class SelfCritiqueAgent:
    """Agente que se auto-critica y mejora iterativamente"""

    def __init__(self):
        # Agente productor
        self.producer = Agent(
            system_prompt="""Eres un productor de contenido de alta calidad.
            Generas contenido bien pensado y completo."""
        )

        # Agente crítico (mismo agente, diferente prompt)
        self.critic = Agent(
            system_prompt="""Eres un crítico riguroso.
            Tu trabajo es identificar problemas y debilidades.
            Sé constructivo pero honesto."""
        )

        self.revision_log: List[CritiqueResult] = []
        self.content_history: List[str] = []

    def generate_initial_content(self, prompt: str) -> str:
        """Genera contenido inicial"""

        print("\n🎯 GENERATING INITIAL CONTENT")
        print("-" * 70)

        generation_prompt = f"""
        Genera contenido para: {prompt}

        Requisitos:
        - Completo y bien estructurado
        - Original y thoughtful
        - Claro y accesible
        - Bien argumentado
        """

        content = self.producer(generation_prompt)
        print(f"Generated:\n{content[:200]}...\n")

        return content

    def critique_content(self, content: str, iteration: int) -> Dict:
        """Critica el contenido generado"""

        print(f"🔍 ITERATION {iteration}: CRITIQUE")
        print("-" * 70)

        critique_prompt = f"""
        Analiza este contenido críticamente:

        ---
        {content}
        ---

        Proporciona:
        1. Puntuación de calidad (0-100)
        2. Principales problemas (máximo 3)
        3. Áreas de mejora
        4. ¿Está listo? (SÍ/NO)

        Sé específico y constructivo.

        Formato:
        PUNTUACIÓN: ...
        PROBLEMAS:
        - ...
        MEJORAS:
        - ...
        LISTO: SÍ/NO
        """

        critique = self.critic(critique_prompt)

        # Parsear crítica
        lines = critique.split('\n')
        score = 70
        problems = []
        improvements = []
        ready = False

        for i, line in enumerate(lines):
            if "PUNTUACIÓN:" in line:
                try:
                    score = int(line.split(":")[-1].strip())
                except:
                    score = 70
            elif line.strip().startswith("- ") and i > 0:
                if "PROBLEMAS" in lines[i-1] or (i > 1 and "PROBLEMAS" in '\n'.join(lines[max(0,i-3):i])):
                    problems.append(line.strip("- "))
                elif "MEJORAS" in lines[i-1] or (i > 1 and "MEJORAS" in '\n'.join(lines[max(0,i-3):i])):
                    improvements.append(line.strip("- "))
            elif "LISTO: SÍ" in line:
                ready = True

        print(f"Score: {score}/100")
        print(f"Problems: {len(problems)}")
        print(f"Ready: {'✓' if ready else '✗'}\n")

        return {
            "critique": critique,
            "score": score,
            "problems": problems,
            "improvements": improvements,
            "ready": ready
        }

    def revise_content(self, content: str, critique_data: Dict) -> str:
        """Revisa el contenido basado en crítica"""

        print(f"✏️  REVISING CONTENT")
        print("-" * 70)

        problems = critique_data.get("problems", [])
        improvements = critique_data.get("improvements", [])

        revision_prompt = f"""
        Contenido anterior:
        ---
        {content}
        ---

        Feedback de crítico:

        Problemas identificados:
        {chr(10).join([f"- {p}" for p in problems])}

        Áreas de mejora:
        {chr(10).join([f"- {i}" for i in improvements])}

        Por favor, revisa el contenido para:
        1. Resolver los problemas identificados
        2. Implementar las mejoras sugeridas
        3. Mantener las fortalezas del original
        4. Mejorar la calidad general

        Proporciona el contenido revisado.
        """

        revised = self.producer(revision_prompt)
        print(f"Revised:\n{revised[:200]}...\n")

        return revised

    def iterative_improvement(self, prompt: str, max_iterations: int = 3, quality_threshold: float = 80):
        """Mejora iterativa del contenido"""

        print(f"\n{'='*70}")
        print(f"SELF-CRITIQUE PATTERN - ITERATIVE IMPROVEMENT")
        print(f"{'='*70}")
        print(f"Max iterations: {max_iterations}")
        print(f"Quality threshold: {quality_threshold}/100\n")

        # Generar inicial
        content = self.generate_initial_content(prompt)
        self.content_history.append(content)

        iteration = 1
        while iteration <= max_iterations:
            # Criticar
            critique_data = self.critique_content(content, iteration)

            # Registrar
            result = CritiqueResult(
                iteration=iteration,
                content=content,
                critique=critique_data["critique"],
                score=critique_data["score"],
                issues_found=critique_data["problems"],
                improvements_made=critique_data["improvements"],
                ready=critique_data["ready"]
            )
            self.revision_log.append(result)

            # Decidir si continuar
            if critique_data["score"] >= quality_threshold or critique_data["ready"]:
                print(f"✓ Quality threshold reached ({critique_data['score']}/100)")
                break

            if iteration >= max_iterations:
                print(f"✗ Max iterations reached")
                break

            # Revisar y preparar siguiente iteración
            content = self.revise_content(content, critique_data)
            self.content_history.append(content)
            iteration += 1

        return content

    def print_improvement_summary(self):
        """Imprime resumen de mejoras"""

        print(f"\n{'='*70}")
        print("IMPROVEMENT SUMMARY")
        print(f"{'='*70}\n")

        if not self.revision_log:
            print("No improvements logged\n")
            return

        print(f"Total Iterations: {len(self.revision_log)}")

        # Progresión de puntuación
        print("\nQuality Progression:")
        for result in self.revision_log:
            bar_length = int(result.score / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  Iteration {result.iteration}: [{bar}] {result.score:.0f}/100")

        # Mejora total
        if len(self.revision_log) > 1:
            initial_score = self.revision_log[0].score
            final_score = self.revision_log[-1].score
            improvement = final_score - initial_score
            print(f"\nTotal Improvement: {improvement:+.0f} points ({final_score:.0f} - {initial_score:.0f})")

        # Problemas resueltos
        print("\nProblems Found Across Iterations:")
        for i, result in enumerate(self.revision_log, 1):
            print(f"  Iteration {i}: {len(result.issues_found)} problems")
            for problem in result.issues_found[:2]:
                print(f"    - {problem}")

        print("\n" + "="*70)
        print("SELF-CRITIQUE PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Mejora iterativa de calidad
  ✓ Auto-corrección
  ✓ Identifica y resuelve problemas
  ✓ Transparencia en proceso
  ✓ Determinístico

Desventajas:
  ✗ Múltiples iteraciones = lentitud
  ✗ Posible convergencia a calidad sub-óptima
  ✗ Costo computacional
  ✗ Riesgo de "conformismo"

Casos de Uso:
  • Mejora de escritura
  • Generación de código
  • Análisis profundo
  • Creative content
  • Quality assurance
        """)


def main():
    """Ejecuta ejemplo del Self-Critique Pattern"""

    agent = SelfCritiqueAgent()

    # Prompt para mejorar iterativamente
    prompt = """
    Escribe un párrafo sobre por qué es importante la educación continua
    en la era de la IA. Debe ser inspirador pero realista.
    """

    # Mejora iterativa
    final_content = agent.iterative_improvement(
        prompt,
        max_iterations=3,
        quality_threshold=75
    )

    # Resumen
    agent.print_improvement_summary()

    # Mostrar versión final
    print(f"\n{'='*70}")
    print("FINAL CONTENT")
    print(f"{'='*70}\n")
    print(final_content)


if __name__ == "__main__":
    main()

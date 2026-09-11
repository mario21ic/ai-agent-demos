"""
AWS Pattern: Basic Reasoning Agent
===================================
Agente que realiza razonamiento básico sobre problemas,
sin acceso a herramientas externas.

Principios AWS:
- Asincrónico: Opera en tiempo
- Autonomía: Toma decisiones independientes
- Agencia: Actúa con propósito para lograr objetivos
"""

from strands import Agent
from typing import Dict, List
import json


class BasicReasoningAgent:
    """Agente que realiza razonamiento sobre un problema"""

    def __init__(self):
        self.agent = Agent(
            system_prompt="""Eres un agente de razonamiento. Tu tarea es:
            1. Analizar problemas complejos
            2. Descomponerlos en partes
            3. Razonar sobre cada parte
            4. Sintetizar una solución

            Proporciona tu razonamiento paso a paso."""
        )

        self.reasoning_log: List[Dict] = []

    def think_through_problem(self, problem: str) -> Dict:
        """Piensa en profundidad sobre un problema"""

        print(f"\n{'='*70}")
        print(f"BASIC REASONING AGENT")
        print(f"{'='*70}\n")

        print(f"Problem: {problem}\n")
        print("Reasoning Process:")
        print("-" * 70)

        # Paso 1: Entender el problema
        understanding_prompt = f"""
        Analiza este problema y explica:
        1. ¿Cuál es el problema central?
        2. ¿Cuáles son los componentes?
        3. ¿Cuáles son las restricciones?

        Problema: {problem}
        """

        understanding = self.agent(understanding_prompt)
        print(f"\n📌 Understanding:\n{understanding}\n")

        # Paso 2: Generar opciones
        options_prompt = f"""
        Basado en el problema: {problem}

        Genera 3 enfoques diferentes para resolver esto:
        - Opción A: ...
        - Opción B: ...
        - Opción C: ...

        Explica cada opción brevemente.
        """

        options = self.agent(options_prompt)
        print(f"💭 Options Generated:\n{options}\n")

        # Paso 3: Evaluar opciones
        evaluation_prompt = f"""
        Opciones consideradas:
        {options}

        Evalúa cada opción en términos de:
        - Viabilidad
        - Impacto
        - Riesgos
        - Tiempo requerido
        """

        evaluation = self.agent(evaluation_prompt)
        print(f"⚖️  Evaluation:\n{evaluation}\n")

        # Paso 4: Seleccionar y justificar
        decision_prompt = f"""
        Basado en tu evaluación anterior:
        {evaluation}

        ¿Cuál es la mejor opción? ¿Por qué?
        Proporciona una recomendación final clara.
        """

        decision = self.agent(decision_prompt)
        print(f"✅ Final Decision:\n{decision}\n")

        # Registrar el razonamiento
        result = {
            "problem": problem,
            "understanding": understanding,
            "options": options,
            "evaluation": evaluation,
            "decision": decision
        }

        self.reasoning_log.append(result)
        return result

    def reason_about_scenario(self, scenario: str) -> str:
        """Razona sobre un escenario hipotético"""

        reasoning_prompt = f"""
        Escenario: {scenario}

        Razona sobre este escenario:
        1. ¿Qué pasaría si...?
        2. ¿Cuáles serían las consecuencias?
        3. ¿Cómo se podría manejar?
        4. ¿Cuáles son los riesgos?

        Proporciona un análisis profundo.
        """

        return self.agent(reasoning_prompt)

    def print_summary(self):
        """Imprime resumen del razonamiento"""

        print(f"\n{'='*70}")
        print("REASONING SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total problems reasoned: {len(self.reasoning_log)}")

        for i, log in enumerate(self.reasoning_log, 1):
            print(f"\n{i}. Problem: {log['problem'][:50]}...")
            print(f"   Depth: Multi-step reasoning with evaluation")
            print(f"   Output: Decision and justification")

        print("\n" + "="*70)
        print("BASIC REASONING AGENT CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ No requiere herramientas externas
  ✓ Razonamiento profundo
  ✓ Explica su pensamiento (interpretable)
  ✓ Útil para problemas abstractos

Desventajas:
  ✗ No accede a información en tiempo real
  ✗ Limitado por conocimiento de entrenamiento
  ✗ Puede tomar mucho tiempo para problemas complejos
  ✗ Riesgo de alucinar información

AWS Principle: AGENCIA
  → El agente actúa con propósito en lugar de humanos
  → Toma decisiones razonadas de forma autónoma
        """)


def main():
    """Ejecuta ejemplo de Basic Reasoning Agent"""

    agent = BasicReasoningAgent()

    # Problema 1: Selección de tecnología
    problem1 = """
    Nuestra startup necesita elegir entre:
    - Monolito escalable con tecnología conocida
    - Microservicios con tecnología nueva
    - Arquitectura sin servidor (serverless)

    Restricciones:
    - Equipo pequeño (5 personas)
    - Presupuesto limitado
    - Time-to-market crítico
    - Necesidad futura de escalabilidad
    """

    result1 = agent.think_through_problem(problem1)

    # Problema 2: Estrategia de datos
    problem2 = """
    ¿Cómo debería una empresa estructurar su estrategia de datos
    considerando GDPR, privacidad, y análisis?
    """

    result2 = agent.think_through_problem(problem2)

    agent.print_summary()


if __name__ == "__main__":
    main()

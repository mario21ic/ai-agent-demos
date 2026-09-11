"""
Judge/Evaluator Agent Pattern
==============================
Un agente "juez" evalúa y valida el trabajo de otros agentes.
Garantiza calidad, consistencia y cumplimiento de estándares.

Use case: Validación de calidad, revisión de código, auditoría, etc.
"""

from strands import Agent
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class JudgmentRating(Enum):
    EXCELLENT = "excellent"  # 5 stars
    GOOD = "good"  # 4 stars
    ACCEPTABLE = "acceptable"  # 3 stars
    POOR = "poor"  # 2 stars
    UNACCEPTABLE = "unacceptable"  # 1 star


@dataclass
class Submission:
    """Una sumisión de un agente para ser juzgada"""
    id: str
    agent_name: str
    task: str
    content: str


@dataclass
class Judgment:
    """Juicio del agente juez"""
    submission_id: str
    rating: JudgmentRating
    strengths: List[str]
    weaknesses: List[str]
    feedback: str
    approved: bool
    score: float  # 0-100


class JudgeAgent:
    """Agente que juzga y valida el trabajo de otros"""

    def __init__(self, standards: Dict[str, str] = None):
        # Agente Juez
        self.judge = Agent(
            system_prompt="""Eres un juez experto y imparcial.
            Tu responsabilidad es:
            1. Evaluar trabajos con criterios claros
            2. Ser justo y constructivo
            3. Proporcionar feedback detallado
            4. Justificar tus decisiones
            5. Mantener estándares altos

            Sé riguroso pero justo."""
        )

        # Agentes productores de contenido
        self.content_creator = Agent(
            system_prompt="Eres creador de contenido. Genera contenido de calidad."
        )

        self.code_generator = Agent(
            system_prompt="Eres un programador. Genera código limpio y eficiente."
        )

        self.analyst = Agent(
            system_prompt="Eres un analista. Realizas análisis profundos y precisos."
        )

        self.standards = standards or {
            "quality": "Alta calidad, sin errores obvios",
            "completeness": "Debe abordar todos los puntos requeridos",
            "clarity": "Debe ser claro y bien organizado",
            "originality": "Debe mostrar pensamiento original",
            "feasibility": "Debe ser implementable/viable"
        }

        self.judgments: List[Judgment] = []
        self.submission_log: List[Dict] = []

    def evaluate_submission(self, submission: Submission) -> Judgment:
        """Evalúa una sumisión"""

        print(f"\n{'='*70}")
        print(f"JUDGING: {submission.id}")
        print(f"Agent: {submission.agent_name}")
        print(f"{'='*70}\n")

        print(f"Submission: {submission.content[:100]}...\n")

        # Fase 1: Análisis de criterios
        print("📊 Analyzing Criteria...")
        print("-" * 70)

        criteria_prompt = f"""
        Evaluando sumisión de {submission.agent_name}

        Tarea: {submission.task}
        Contenido: {submission.content}

        Criterios de evaluación:
        {chr(10).join([f"- {k}: {v}" for k, v in self.standards.items()])}

        Evalúa cada criterio:
        1. ¿Se cumple este criterio?
        2. Qué evidencia hay?
        3. Qué tan bien se cumple?
        """

        criteria_analysis = self.judge(criteria_prompt)
        print(f"Analysis:\n{criteria_analysis[:200]}...\n")

        # Fase 2: Fortalezas y debilidades
        print("💪 Identifying Strengths and Weaknesses...")
        print("-" * 70)

        feedback_prompt = f"""
        Basado en tu análisis anterior:

        {criteria_analysis}

        Proporciona:
        1. Las 3 fortalezas principales
        2. Las 3 debilidades principales
        3. Un feedback constructivo de una frase
        4. Una calificación de 1-5 estrellas

        Formato:
        FORTALEZAS:
        - ...

        DEBILIDADES:
        - ...

        FEEDBACK: ...

        RATING: X/5
        """

        feedback = self.judge(feedback_prompt)

        # Parsear feedback
        lines = feedback.split('\n')
        strengths = []
        weaknesses = []
        feedback_text = ""
        rating_str = "3"

        for line in lines:
            if "FORTALEZAS" in line:
                strengths_mode = True
            elif "DEBILIDADES" in line:
                weaknesses_mode = True
            elif "FEEDBACK:" in line:
                feedback_text = line.replace("FEEDBACK:", "").strip()
            elif "RATING:" in line:
                rating_str = line.replace("RATING:", "").split('/')[0].strip()

        # Convertir rating
        try:
            rating_score = int(rating_str)
        except:
            rating_score = 3

        rating_map = {1: JudgmentRating.UNACCEPTABLE, 2: JudgmentRating.POOR,
                      3: JudgmentRating.ACCEPTABLE, 4: JudgmentRating.GOOD,
                      5: JudgmentRating.EXCELLENT}
        judgment_rating = rating_map.get(rating_score, JudgmentRating.ACCEPTABLE)

        print(f"Feedback:\n{feedback[:200]}...\n")

        # Fase 3: Decisión final
        print("✅ Final Judgment...")
        print("-" * 70)

        decision_prompt = f"""
        Basado en todo tu análisis:

        Rating: {judgment_rating.value}
        Feedback: {feedback_text}

        ¿Debería ser APROBADO o RECHAZADO?
        Proporciona tu decisión final con justificación clara.
        """

        decision = self.judge(decision_prompt)
        approved = "aprobado" in decision.lower() or "approved" in decision.lower()

        print(f"Decision: {'✓ APPROVED' if approved else '✗ REJECTED'}\n")

        # Crear juicio
        judgment = Judgment(
            submission_id=submission.id,
            rating=judgment_rating,
            strengths=strengths,
            weaknesses=weaknesses,
            feedback=feedback_text,
            approved=approved,
            score=(rating_score / 5.0) * 100
        )

        self.judgments.append(judgment)

        # Registrar
        self.submission_log.append({
            "submission": submission,
            "judgment": judgment
        })

        return judgment

    def batch_judge(self, submissions: List[Submission]) -> List[Judgment]:
        """Juzga múltiples sumisiones"""

        print(f"\n{'='*70}")
        print(f"BATCH JUDGMENT - {len(submissions)} submissions")
        print(f"{'='*70}\n")

        results = []
        for submission in submissions:
            judgment = self.evaluate_submission(submission)
            results.append(judgment)

        return results

    def print_judgment_summary(self):
        """Imprime resumen de los juicios"""

        print(f"\n{'='*70}")
        print("JUDGE AGENT SUMMARY")
        print(f"{'='*70}\n")

        if not self.judgments:
            print("No judgments yet\n")
            return

        # Estadísticas
        total = len(self.judgments)
        approved = len([j for j in self.judgments if j.approved])
        rejected = total - approved

        print(f"Total Judgments: {total}")
        print(f"Approved: {approved} ({approved/total*100:.0f}%)")
        print(f"Rejected: {rejected} ({rejected/total*100:.0f}%)\n")

        # Por rating
        print("Distribution by Rating:")
        for rating in JudgmentRating:
            count = len([j for j in self.judgments if j.rating == rating])
            bar = "█" * count + "░" * (total - count)
            print(f"  {rating.value:15} [{bar}] {count}")

        # Promedio de score
        avg_score = sum([j.score for j in self.judgments]) / total
        print(f"\nAverage Score: {avg_score:.1f}/100")

        print("\n" + "="*70)
        print("JUDGE PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Garantiza calidad y consistencia
  ✓ Feedback constructivo
  ✓ Imparcial y objetivo
  ✓ Establece estándares
  ✓ Previene errores

Desventajas:
  ✗ Agrega latencia
  ✗ Puede ser lento
  ✗ Requiere criterios claros
  ✗ Falsos positivos/negativos

Casos de Uso:
  • Validación de calidad
  • Revisión de código
  • Auditoría
  • Control de contenido
  • Aprobación de decisiones
        """)


def main():
    """Ejecuta ejemplo del Judge Pattern"""

    judge = JudgeAgent()

    # Crear sumisiones de prueba
    submissions = [
        Submission(
            id="s1",
            agent_name="Content Creator",
            task="Escribir un artículo sobre IA",
            content="La IA es un campo fascinante que transforma la tecnología..."
        ),
        Submission(
            id="s2",
            agent_name="Code Generator",
            task="Generar función de suma",
            content="def suma(a, b): return a + b"
        ),
        Submission(
            id="s3",
            agent_name="Analyst",
            task="Analizar tendencias de mercado",
            content="El mercado muestra crecimiento del 15% en Q3..."
        ),
    ]

    # Juzgar todas
    judge.batch_judge(submissions)

    # Resumen
    judge.print_judgment_summary()


if __name__ == "__main__":
    main()

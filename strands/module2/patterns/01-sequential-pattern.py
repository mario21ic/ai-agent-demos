"""
Sequential Agent Pattern
========================
Los agentes se ejecutan uno después del otro en secuencia.
La salida de un agente es entrada del siguiente.

Use case: Procesamiento de documentos, análisis en fases, etc.
"""

from strands import Agent
from typing import List


class SequentialPipeline:
    """Pipeline secuencial de agentes"""

    def __init__(self):
        # Agente 1: Research
        self.researcher = Agent(
            system_prompt="""Eres un investigador. Tu tarea es analizar un tema
            y proporcionar hechos clave, puntos principales y preguntas importantes."""
        )

        # Agente 2: Analyst
        self.analyst = Agent(
            system_prompt="""Eres un analista de datos. Tu tarea es tomar información
            de un investigador y crear un análisis estructurado con insights."""
        )

        # Agente 3: Writer
        self.writer = Agent(
            system_prompt="""Eres un escritor profesional. Tu tarea es tomar un análisis
            y convertirlo en un documento bien estructurado y legible."""
        )

        # Agente 4: Editor
        self.editor = Agent(
            system_prompt="""Eres un editor. Tu tarea es revisar el documento final,
            corregir errores y mejorar la claridad."""
        )

        self.pipeline_log: List[dict] = []

    def run_sequential(self, topic: str) -> str:
        """Ejecuta la pipeline secuencial"""

        print(f"\n{'='*70}")
        print(f"SEQUENTIAL PIPELINE: {topic}")
        print(f"{'='*70}\n")

        # PASO 1: Research
        print("📚 PASO 1: Investigación")
        print("-" * 70)
        research = self.researcher(f"Investiga sobre: {topic}")
        self.pipeline_log.append({"stage": "Research", "output": research})
        print(f"Research completada\n")

        # PASO 2: Analysis
        print("📊 PASO 2: Análisis")
        print("-" * 70)
        analysis = self.analyst(
            f"Basado en esta investigación, crea un análisis:\n{research}"
        )
        self.pipeline_log.append({"stage": "Analysis", "output": analysis})
        print(f"Análisis completado\n")

        # PASO 3: Writing
        print("✍️  PASO 3: Redacción")
        print("-" * 70)
        document = self.writer(
            f"Escribe un documento basado en este análisis:\n{analysis}"
        )
        self.pipeline_log.append({"stage": "Writing", "output": document})
        print(f"Documento redactado\n")

        # PASO 4: Editing
        print("✏️  PASO 4: Edición")
        print("-" * 70)
        final = self.editor(
            f"Edita y mejora este documento:\n{document}"
        )
        self.pipeline_log.append({"stage": "Editing", "output": final})
        print(f"Edición completada\n")

        return final

    def print_summary(self):
        """Imprime resumen del pipeline"""

        print(f"\n{'='*70}")
        print("PIPELINE SUMMARY")
        print(f"{'='*70}\n")

        stages = [
            ("🔬", "Research", "Recolecta información"),
            ("📈", "Analysis", "Analiza los datos"),
            ("📝", "Writing", "Redacta documento"),
            ("🔍", "Editing", "Revisa y mejora"),
        ]

        for i, (emoji, stage, desc) in enumerate(stages, 1):
            status = "✓" if i <= len(self.pipeline_log) else "✗"
            print(f"{status} {emoji} Paso {i}: {stage}")
            print(f"   {desc}")
            if i <= len(self.pipeline_log):
                output_preview = self.pipeline_log[i-1]["output"][:100] + "..."
                print(f"   Output: {output_preview}")
            print()

        print("\n" + "="*70)
        print("FLUJO SECUENCIAL COMPLETADO")
        print("="*70)
        print("""
Características del patrón secuencial:
  ✓ Cada agente espera a que el anterior termine
  ✓ La salida de uno es entrada del siguiente
  ✓ Facilita debugging (se ve dónde falló)
  ✓ Ideal para pipelines de procesamiento

Desventajas:
  ✗ Lento si hay muchos agentes
  ✗ Un fallo detiene todo el pipeline
  ✗ No aprovecha paralelismo
        """)


def main():
    """Ejecuta ejemplo del patrón secuencial"""

    pipeline = SequentialPipeline()

    topic = "Inteligencia Artificial en Educación"
    result = pipeline.run_sequential(topic)

    print(f"\n{'='*70}")
    print("DOCUMENTO FINAL")
    print(f"{'='*70}\n")
    print(result)

    pipeline.print_summary()


if __name__ == "__main__":
    main()

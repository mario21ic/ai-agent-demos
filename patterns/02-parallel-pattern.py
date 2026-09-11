"""
Parallel Agent Pattern
======================
Múltiples agentes ejecutan tareas simultáneamente en paralelo.
Útil cuando las tareas son independientes.

Use case: Análisis desde múltiples ángulos, recolección de datos, etc.
"""

from strands import Agent
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
import time


class ParallelTeam:
    """Equipo de agentes ejecutando en paralelo"""

    def __init__(self):
        # Especialistas
        self.technical_expert = Agent(
            system_prompt="""Eres un experto técnico. Analiza desde una perspectiva
            técnica y de implementación."""
        )

        self.business_expert = Agent(
            system_prompt="""Eres un experto en negocios. Analiza desde una perspectiva
            de valor comercial y ROI."""
        )

        self.security_expert = Agent(
            system_prompt="""Eres un experto en seguridad. Analiza desde una perspectiva
            de riesgos y seguridad."""
        )

        self.ux_expert = Agent(
            system_prompt="""Eres un experto en UX. Analiza desde una perspectiva
            de experiencia de usuario."""
        )

        self.results: Dict[str, str] = {}
        self.execution_times: Dict[str, float] = {}

    def analyze_technical(self, topic: str) -> str:
        """Análisis técnico"""
        start = time.time()
        result = self.technical_expert(
            f"Analiza desde perspectiva técnica: {topic}\nDa 3 puntos técnicos clave."
        )
        self.execution_times["Technical"] = time.time() - start
        return result

    def analyze_business(self, topic: str) -> str:
        """Análisis de negocio"""
        start = time.time()
        result = self.business_expert(
            f"Analiza desde perspectiva comercial: {topic}\nDa 3 puntos de negocio clave."
        )
        self.execution_times["Business"] = time.time() - start
        return result

    def analyze_security(self, topic: str) -> str:
        """Análisis de seguridad"""
        start = time.time()
        result = self.security_expert(
            f"Analiza desde perspectiva de seguridad: {topic}\nDa 3 riesgos principales."
        )
        self.execution_times["Security"] = time.time() - start
        return result

    def analyze_ux(self, topic: str) -> str:
        """Análisis de UX"""
        start = time.time()
        result = self.ux_expert(
            f"Analiza desde perspectiva de UX: {topic}\nDa 3 consideraciones de UX."
        )
        self.execution_times["UX"] = time.time() - start
        return result

    def run_parallel_analysis(self, topic: str) -> Dict[str, str]:
        """Ejecuta análisis en paralelo"""

        print(f"\n{'='*70}")
        print(f"PARALLEL ANALYSIS: {topic}")
        print(f"{'='*70}\n")

        start_total = time.time()

        # Ejecutar en paralelo
        with ThreadPoolExecutor(max_workers=4) as executor:
            print("🚀 Iniciando 4 análisis en paralelo...\n")

            # Lanzar todas las tareas
            future_technical = executor.submit(self.analyze_technical, topic)
            future_business = executor.submit(self.analyze_business, topic)
            future_security = executor.submit(self.analyze_security, topic)
            future_ux = executor.submit(self.analyze_ux, topic)

            # Esperar resultados
            print("⏳ Esperando resultados...\n")

            self.results["Technical"] = future_technical.result()
            self.results["Business"] = future_business.result()
            self.results["Security"] = future_security.result()
            self.results["UX"] = future_ux.result()

            print("✓ Todos los análisis completados\n")

        total_time = time.time() - start_total

        return {
            "results": self.results,
            "total_time": total_time,
            "execution_times": self.execution_times
        }

    def print_results(self):
        """Imprime resultados en paralelo"""

        print(f"\n{'='*70}")
        print("PARALLEL ANALYSIS RESULTS")
        print(f"{'='*70}\n")

        experts = [
            ("🔧", "Technical", "Análisis Técnico"),
            ("💼", "Business", "Análisis de Negocio"),
            ("🔐", "Security", "Análisis de Seguridad"),
            ("🎨", "UX", "Análisis de UX"),
        ]

        for emoji, key, title in experts:
            print(f"{emoji} {title}")
            print("-" * 70)
            if key in self.results:
                output = self.results[key][:150] + "..."
                print(f"{output}")
                if key in self.execution_times:
                    print(f"Tiempo: {self.execution_times[key]:.2f}s")
            print()

    def print_performance_summary(self, total_time: float):
        """Compara rendimiento secuencial vs paralelo"""

        print(f"\n{'='*70}")
        print("PERFORMANCE COMPARISON")
        print(f"{'='*70}\n")

        individual_times = sum(self.execution_times.values())

        print(f"⏱️  Tiempo Individual (suma):    {individual_times:.2f}s")
        print(f"⏱️  Tiempo Total (paralelo):    {total_time:.2f}s")
        print(f"⏩ Aceleración:                {individual_times/total_time:.2f}x\n")

        print("Desglose por experto:")
        for expert, elapsed in self.execution_times.items():
            bar_length = int((elapsed / individual_times) * 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            print(f"  {expert:12} [{bar}] {elapsed:.2f}s")

        print("\n" + "="*70)
        print("VENTAJAS DEL PATRÓN PARALELO")
        print("="*70)
        print(f"""
✓ Aceleración: {individual_times/total_time:.2f}x más rápido que secuencial
✓ Máxima utilización de recursos
✓ Ideal para análisis desde múltiples ángulos
✓ Escalable a más agentes

Desventajas:
✗ Más complejo de implementar
✗ Requiere sincronización
✗ Difícil de debuggear si falla uno
        """)


def main():
    """Ejecuta ejemplo del patrón paralelo"""

    team = ParallelTeam()

    topic = "Implementar un Sistema de Microservicios"
    result = team.run_parallel_analysis(topic)

    team.print_results()
    team.print_performance_summary(result["total_time"])


if __name__ == "__main__":
    main()

"""
Specialist Agent Pattern
=========================
Cada agente es especialista en un dominio específico.
Agentes colaboran combinando sus expertisas para resolver problemas complejos.

Use case: Equipos de expertos, consultoría, resolución de problemas complejos, etc.
"""

from strands import Agent
from typing import Dict, List
from abc import ABC, abstractmethod


class Specialist(ABC):
    """Base class para especialistas"""

    def __init__(self, name: str, domain: str, system_prompt: str):
        self.name = name
        self.domain = domain
        self.agent = Agent(system_prompt=system_prompt)
        self.expertise_areas: List[str] = []
        self.consultations: List[str] = []

    @abstractmethod
    def analyze(self, problem: str) -> str:
        """Analiza un problema desde su especialidad"""
        pass

    def consult(self, question: str) -> str:
        """Responde una consulta de otro especialista"""
        response = self.agent(question)
        self.consultations.append(response)
        return response


class ArchitectSpecialist(Specialist):
    """Especialista en Arquitectura de Software"""

    def __init__(self):
        super().__init__(
            name="Software Architect",
            domain="Architecture",
            system_prompt="""Eres un arquitecto de software experto.
            Te especializas en: diseño de sistemas, patrones arquitectónicos,
            escalabilidad, mantenibilidad. Proporciona recomendaciones
            de arquitectura de alto nivel."""
        )
        self.expertise_areas = ["Design Patterns", "Scalability", "System Design", "Microservices"]

    def analyze(self, problem: str) -> str:
        prompt = f"Como arquitecto, analiza este problema de diseño: {problem}"
        return self.agent(prompt)


class DatabaseSpecialist(Specialist):
    """Especialista en Bases de Datos"""

    def __init__(self):
        super().__init__(
            name="Database Expert",
            domain="Databases",
            system_prompt="""Eres un experto en bases de datos.
            Te especializas en: modelado de datos, optimización de queries,
            replicación, backups. Proporciona recomendaciones sobre
            estrategias de bases de datos."""
        )
        self.expertise_areas = ["Data Modeling", "Query Optimization", "Replication", "Performance"]

    def analyze(self, problem: str) -> str:
        prompt = f"Como experto en bases de datos, analiza este problema: {problem}"
        return self.agent(prompt)


class SecuritySpecialist(Specialist):
    """Especialista en Seguridad"""

    def __init__(self):
        super().__init__(
            name="Security Expert",
            domain="Security",
            system_prompt="""Eres un experto en ciberseguridad.
            Te especializas en: análisis de vulnerabilidades, encriptación,
            autenticación, autorización, compliance. Proporciona
            recomendaciones de seguridad."""
        )
        self.expertise_areas = ["Vulnerability Assessment", "Encryption", "Authentication", "Compliance"]

    def analyze(self, problem: str) -> str:
        prompt = f"Como experto en seguridad, analiza este problema: {problem}"
        return self.agent(prompt)


class PerformanceSpecialist(Specialist):
    """Especialista en Performance"""

    def __init__(self):
        super().__init__(
            name="Performance Expert",
            domain="Performance",
            system_prompt="""Eres un experto en optimización de performance.
            Te especializas en: profiling, caching, parallelización,
            bottlenecks, benchmarking. Proporciona recomendaciones
            para mejorar performance."""
        )
        self.expertise_areas = ["Profiling", "Caching", "Parallelization", "Benchmarking"]

    def analyze(self, problem: str) -> str:
        prompt = f"Como experto en performance, analiza este problema: {problem}"
        return self.agent(prompt)


class SpecialistConsultancy:
    """Consultoría con equipo de especialistas"""

    def __init__(self):
        self.architect = ArchitectSpecialist()
        self.database = DatabaseSpecialist()
        self.security = SecuritySpecialist()
        self.performance = PerformanceSpecialist()

        self.specialists = [
            self.architect,
            self.database,
            self.security,
            self.performance
        ]

        self.coordinator = Agent(
            system_prompt="""Eres un coordinador de consultoría.
            Tu rol es sintetizar los análisis de múltiples especialistas
            en una recomendación unificada y coherente."""
        )

        self.consultation_log: List[Dict] = []

    def get_specialist_analyses(self, problem: str) -> Dict[str, str]:
        """Obtiene análisis de todos los especialistas"""

        print(f"\n{'='*70}")
        print("SPECIALIST ANALYSES")
        print(f"{'='*70}\n")

        analyses = {}

        for specialist in self.specialists:
            print(f"🔍 {specialist.name} ({specialist.domain})")
            print("-" * 70)

            analysis = specialist.analyze(problem)
            analyses[specialist.name] = analysis

            print(f"Expertise areas: {', '.join(specialist.expertise_areas)}")
            print(f"Analysis: {analysis[:150]}...")
            print()

        return analyses

    def specialist_cross_consultation(self, problem: str):
        """Especialistas consultan entre sí"""

        print(f"\n{'='*70}")
        print("CROSS-SPECIALIST CONSULTATION")
        print(f"{'='*70}\n")

        # El arquitecto pregunta al DB specialist
        print("🏗️  Architect → Database Specialist:")
        db_response = self.database.consult(
            f"Para este problema de arquitectura: {problem}\n"
            f"¿Qué estrategia de datos me recomiendas?"
        )
        print(f"  {db_response[:100]}...\n")

        # El DB specialist pregunta al Security specialist
        print("🔐 Database → Security Specialist:")
        sec_response = self.security.consult(
            f"Para la estrategia de datos propuesta,\n"
            f"¿cuáles son las consideraciones de seguridad?"
        )
        print(f"  {sec_response[:100]}...\n")

        # El Security specialist pregunta al Performance specialist
        print("⚡ Security → Performance Specialist:")
        perf_response = self.performance.consult(
            f"Las medidas de seguridad propuestas,\n"
            f"¿cómo afectarán la performance?"
        )
        print(f"  {perf_response[:100]}...\n")

    def synthesize_recommendation(self, problem: str, analyses: Dict[str, str]) -> str:
        """Sintetiza todas las perspectivas en una recomendación"""

        print(f"\n{'='*70}")
        print("COORDINATOR SYNTHESIS")
        print(f"{'='*70}\n")

        analyses_text = "\n".join([
            f"{name}:\n{analysis[:200]}..."
            for name, analysis in analyses.items()
        ])

        prompt = f"""
        Problema: {problem}

        Análisis de especialistas:
        {analyses_text}

        Sintetiza estos análisis en:
        1. Recomendación arquitectónica principal
        2. Consideraciones críticas de seguridad
        3. Estrategia de datos y performance
        4. Plan de implementación de alto nivel
        """

        recommendation = self.coordinator(prompt)
        self.consultation_log.append({
            "problem": problem,
            "analyses": analyses,
            "recommendation": recommendation
        })

        return recommendation

    def run_full_consultation(self, problem: str):
        """Ejecuta consultoría completa"""

        print(f"\n{'='*70}")
        print(f"SPECIALIST CONSULTANCY SESSION")
        print(f"{'='*70}\n")
        print(f"Problem: {problem}\n")

        # Obtener análisis
        analyses = self.get_specialist_analyses(problem)

        # Consultas cruzadas
        self.specialist_cross_consultation(problem)

        # Síntesis
        recommendation = self.synthesize_recommendation(problem, analyses)

        print("🎯 FINAL RECOMMENDATION:")
        print("-" * 70)
        print(recommendation)

        return recommendation

    def print_specialist_profiles(self):
        """Imprime perfiles de especialistas"""

        print(f"\n{'='*70}")
        print("SPECIALIST TEAM PROFILES")
        print(f"{'='*70}\n")

        for specialist in self.specialists:
            print(f"👤 {specialist.name}")
            print(f"   Domain: {specialist.domain}")
            print(f"   Expertise Areas:")
            for area in specialist.expertise_areas:
                print(f"     • {area}")
            print(f"   Consultations Given: {len(specialist.consultations)}")
            print()

        print("\n" + "="*70)
        print("SPECIALIST PATTERN CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Profundidad de expertise
  ✓ Soluciones completas y bien informadas
  ✓ Cada especialista hace lo suyo mejor
  ✓ Fácil añadir nuevos especialistas
  ✓ Recomendaciones balanceadas

Desventajas:
  ✗ Requiere mucha coordinación
  ✗ Puede ser lento
  ✗ Necesita buenos mecanismos de comunicación
  ✗ Caro en recursos
        """)


def main():
    """Ejecuta ejemplo del patrón de especialistas"""

    consultancy = SpecialistConsultancy()

    problem = """
    Necesitamos diseñar un sistema de e-commerce escalable que:
    - Maneje millones de transacciones diarias
    - Proteja datos sensibles de usuarios
    - Garantice máxima uptime (99.99%)
    - Sea mantenible y extensible a largo plazo
    """

    consultancy.run_full_consultation(problem)
    consultancy.print_specialist_profiles()


if __name__ == "__main__":
    main()

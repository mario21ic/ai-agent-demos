"""
Agent-to-Agent with Tools
==========================
Agentes que se comunican y usan herramientas externas
"""

from strands import Agent
from strands_tools import http_request, current_time
import json


class AgentWithTools:
    """Gestión de comunicación A2A con herramientas"""

    def __init__(self):
        # Agent 1: Researcher con acceso a herramientas
        self.researcher = Agent(
            system_prompt="""You are a researcher who investigates current tech topics.
            You use tools to gather information and then formulate intelligent questions.""",
            tools=[current_time, http_request]
        )

        # Agent 2: Analyst que procesa información
        self.analyst = Agent(
            system_prompt="""You are a data analyst. You receive questions and raw information,
            then provide structured analysis and insights."""
        )

    def research_phase(self, topic: str) -> str:
        """Fase 1: Researcher recopila información"""
        print("\n📊 RESEARCH PHASE")
        print("-" * 40)

        prompt = f"""
        Investigate current information about '{topic}'.
        Use the http_request tool to search for recent information.
        Format your findings as a summary with key points.
        """

        research_result = self.researcher(prompt)
        print(f"Research findings:\n{research_result}\n")
        return research_result

    def analysis_phase(self, research_data: str) -> str:
        """Fase 2: Analyst analiza los datos"""
        print("📈 ANALYSIS PHASE")
        print("-" * 40)

        prompt = f"""
        Based on this research data, provide a structured analysis:

        Data:
        {research_data}

        Please provide:
        1. Key patterns identified
        2. Main insights
        3. Recommendations
        """

        analysis = self.analyst(prompt)
        print(f"Analysis:\n{analysis}\n")
        return analysis

    def validation_phase(self, analysis: str) -> str:
        """Fase 3: Researcher valida y formula preguntas finales"""
        print("✅ VALIDATION PHASE")
        print("-" * 40)

        prompt = f"""
        Review this analysis and identify any gaps or areas needing clarification.
        Formulate critical follow-up questions:

        Analysis:
        {analysis}
        """

        validation = self.researcher(prompt)
        print(f"Validation & follow-up questions:\n{validation}\n")
        return validation


def main():
    """Ejecuta demostración A2A con herramientas"""
    print("\n" + "="*60)
    print("AGENT-TO-AGENT WITH TOOLS")
    print("="*60)

    a2a = AgentWithTools()

    topic = "Machine Learning trends in 2024"

    # Ejecutar fases
    research = a2a.research_phase(topic)
    analysis = a2a.analysis_phase(research)
    validation = a2a.validation_phase(analysis)

    # Resumen final
    print("\n" + "="*60)
    print("WORKFLOW COMPLETED")
    print("="*60)
    print("✓ Research completed")
    print("✓ Analysis provided")
    print("✓ Validation performed")


if __name__ == "__main__":
    main()

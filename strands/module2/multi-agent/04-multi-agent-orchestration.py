"""
Multi-Agent Orchestration
==========================
Múltiples agentes especializados que se comunican entre sí
"""

from strands import Agent
from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    sender: str
    recipient: str
    content: str


class MultiAgentTeam:
    """Equipo de agentes especializados comunicándose"""

    def __init__(self):
        self.message_log: List[Message] = []

        # Agent 1: Product Manager
        self.pm = Agent(
            system_prompt="""You are a Product Manager. Define requirements and features
            clearly based on user needs. Communicate with team leads."""
        )

        # Agent 2: Tech Lead
        self.tech_lead = Agent(
            system_prompt="""You are a Tech Lead. You evaluate feasibility of requirements,
            propose architecture, and communicate with PM and engineers."""
        )

        # Agent 3: Engineer
        self.engineer = Agent(
            system_prompt="""You are a Software Engineer. You implement features and report
            on technical challenges and timelines to the tech lead."""
        )

        # Agent 4: QA Lead
        self.qa = Agent(
            system_prompt="""You are a QA Lead. You ensure quality by testing features
            and identifying edge cases. Communicate issues to PM and engineers."""
        )

    def send_message(self, sender: str, recipient: str, content: str) -> str:
        """Envía mensaje de un agente a otro"""
        agent_map = {
            "pm": self.pm,
            "tech_lead": self.tech_lead,
            "engineer": self.engineer,
            "qa": self.qa
        }

        recipient_agent = agent_map.get(recipient)
        if not recipient_agent:
            return "Recipient not found"

        # El agente receptor responde
        context = f"Message from {sender}: {content}\n\nRespond professionally and concisely."
        response = recipient_agent(context)

        # Log del mensaje
        self.message_log.append(Message(sender=sender, recipient=recipient, content=content))

        return response

    def product_planning_meeting(self):
        """Simulación de reunión de planificación de producto"""
        print("\n" + "="*60)
        print("PRODUCT PLANNING MEETING")
        print("="*60 + "\n")

        # PM presenta idea
        print("👔 PM: Proposing new feature...")
        feature_idea = self.pm("Define a new feature for an e-commerce platform")
        print(f"Feature Proposal:\n{feature_idea}\n")

        # Tech Lead evalúa
        print("👨‍💼 TECH LEAD: Evaluating feasibility...")
        feasibility = self.send_message(
            "pm", "tech_lead",
            f"Evaluate this feature: {feature_idea}"
        )
        print(f"Tech Assessment:\n{feasibility}\n")

        # Engineer estima esfuerzo
        print("👨‍💻 ENGINEER: Estimating implementation...")
        estimate = self.send_message(
            "tech_lead", "engineer",
            f"Based on this requirement, estimate effort and challenges:\n{feasibility}"
        )
        print(f"Implementation Plan:\n{estimate}\n")

        # QA verifica testabilidad
        print("🧪 QA: Planning tests...")
        test_plan = self.send_message(
            "engineer", "qa",
            f"Based on this implementation plan, what test cases do we need?\n{estimate}"
        )
        print(f"QA Strategy:\n{test_plan}\n")

        # PM recibe feedback
        print("👔 PM: Receiving final assessment...")
        final_feedback = self.send_message(
            "qa", "pm",
            f"Here's our testing strategy and any concerns:\n{test_plan}\n\nProvide final approval decision."
        )
        print(f"PM Decision:\n{final_feedback}\n")

    def print_communication_log(self):
        """Imprime log de comunicaciones"""
        print("\n" + "="*60)
        print("COMMUNICATION LOG")
        print("="*60 + "\n")

        for i, msg in enumerate(self.message_log, 1):
            print(f"{i}. {msg.sender.upper()} → {msg.recipient.upper()}")
            print(f"   Message: {msg.content[:100]}...\n")


def main():
    """Ejecuta simulación de equipo multi-agente"""
    team = MultiAgentTeam()
    team.product_planning_meeting()
    team.print_communication_log()


if __name__ == "__main__":
    main()

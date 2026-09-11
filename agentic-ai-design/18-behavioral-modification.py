"""Pattern 18: Behavioral Modification Pattern"""
from strands import Agent

class BehavioralModificationPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres adaptable al feedback")
        self.behavior_score = 0.5

    def adapt_behavior(self, feedback: str):
        print(f"\n{'='*70}\nBEHAVIORAL MODIFICATION\n{'='*70}\n")

        if "bueno" in feedback.lower() or "good" in feedback.lower():
            self.behavior_score += 0.1
            print(f"✓ Comportamiento mejorado")
        else:
            self.behavior_score -= 0.1
            print(f"✗ Comportamiento ajustado")

        self.behavior_score = max(0, min(1, self.behavior_score))
        print(f"  Puntuación: {self.behavior_score:.1f}\n")

    def get_adapted_response(self, query: str) -> str:
        if self.behavior_score > 0.7:
            prompt = f"(Modo positivo y entusiasta) {query}"
        elif self.behavior_score < 0.3:
            prompt = f"(Modo cauteloso y prudente) {query}"
        else:
            prompt = f"(Modo equilibrado) {query}"

        return str(self.agent(prompt))

def main():
    pattern = BehavioralModificationPattern()
    pattern.adapt_behavior("Tu respuesta anterior fue excelente")
    pattern.adapt_behavior("Necesitas ser más cuidadoso")
    result = pattern.get_adapted_response("¿Cuál es tu análisis?")
    print(f"Respuesta adaptada: {result[:150]}...\n")

if __name__ == "__main__":
    main()
